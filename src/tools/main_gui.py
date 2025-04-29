import os, io, wave, threading, asyncio, queue, time, tkinter as tk
from tkinter import ttk
import numpy as np
import pyaudio, pvcobra

# ---- import your existing logic (same file-names you already use) ----
from intro_conversational_tool import (
    recite_model_response,
    Response,
    AzureChatOpenAI,
    JsonOutputParser,
    PromptTemplate,
    AIMessage,
    HumanMessage,
    get_buffer_string,
    run_agent, onboarding_agent
)

# -------------  SMALL UTIL: non-blocking, stoppable recorder -----------
def record_and_transcribe(stop_event: threading.Event) -> str:
    """
    Same as your old function, but returns "" immediately if stop_event is set.
    """
    cobra = pvcobra.create(access_key="KFgQP1ckC6l64TJ61gWrPaCeh5Es7lsTTD4f1Jg1QaOTSrelnx+iow==")
    FORMAT, CHANNELS, RATE, FRAMES_PER_BUFFER = pyaudio.paInt16, 1, 16000, 512
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                        frames_per_buffer=FRAMES_PER_BUFFER, input=True)
    frames, pause_seconds = [], 3
    nbuffers = int(np.ceil(1 / (FRAMES_PER_BUFFER / RATE) * pause_seconds))

    try:
        counter = 0
        while not stop_event.is_set():
            data = stream.read(FRAMES_PER_BUFFER, exception_on_overflow=False)
            audio_frame = np.frombuffer(data, dtype=np.int16)
            frames.append(audio_frame)
            prob = cobra.process(audio_frame)
            counter = counter + 1 if prob < 0.1 else 0
            if counter >= nbuffers:
                break
    finally:
        stream.stop_stream(); stream.close(); audio.terminate(); cobra.delete()

    if stop_event.is_set():
        return ""          # user aborted

    # ----- transcription with Azure Whisper (unchanged) ---------------
    wav_bytes = io.BytesIO()
    with wave.open(wav_bytes, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(np.concatenate(frames).tobytes())
    wav_bytes.seek(0)

    import requests
    r = requests.post(
        os.getenv("AZURE_WHISPER_ENDPOINT"),
        headers={"api-key": os.getenv("AZURE_WHISPER_KEY")},
        files={"file": ("audio.wav", wav_bytes, "audio/wav")},
    )
    return "" if r.status_code != 200 else r.json().get("text", "")

# -----------------------------  GUI ------------------------------------
BG, FG = "#101010", "#ffffff"
root = tk.Tk(); root.title("Kala Copilot"); root.configure(bg=BG)
root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")

ttk.Style().configure("TLabel", background=BG, foreground=FG)
title_lbl = ttk.Label(root, text="Kala Copilot", font=("Segoe UI", 18, "bold"))
title_lbl.place(x=20, y=15)

msg_lbl = ttk.Label(root, text="Press  Start  to begin …",
                    font=("Segoe UI", 32, "bold"),
                    anchor="center", justify="center",
                    wraplength=root.winfo_screenwidth() - 100)
msg_lbl.place(relx=0.5, rely=0.5, anchor="center")

start_btn = ttk.Button(root, text="Start")
stop_btn  = ttk.Button(root, text="Stop")
start_btn.place(relx=0.45, rely=0.9, anchor="center")
stop_btn .place(relx=0.55, rely=0.9, anchor="center")
stop_btn .config(state=tk.DISABLED)

# ---------------  conversation thread & control flags -----------------
stop_event   = threading.Event()
thread_alive = threading.Event()      # just to know when finished
conv_history = ""                     # will be filled at the end

def update_message(text): msg_lbl.config(text=text)

def conversational_loop():
    """
    Runs in a background thread.  Reads / writes stop_event,
    sets thread_alive when done.
    """
    global conv_history
    conversation_history = []

    with open(r"src\tools\prompts\OnboardingMayaPrompt.txt", encoding="utf-8") as f:
        prompt_template = f.read()

    parser = JsonOutputParser(pydantic_object=Response)
    chain = (PromptTemplate(
                template=prompt_template,
                input_variables=["conversation_history"],
                partial_variables={"format_instructions": parser.get_format_instructions()})
             | AzureChatOpenAI(
                openai_api_key=os.getenv("AZURE_OPENAI_KEY"),
                azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
                openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION"))
             | parser)

    while not stop_event.is_set():
        resp = chain.invoke({"conversation_history": conversation_history})
        conversation_history.append(AIMessage(content=resp["message"]))

        root.after(0, update_message, resp["message"])
        recite_model_response(resp["message"])

        if resp["end_of_conversation"]:
            break

        user_txt = record_and_transcribe(stop_event)
        if stop_event.is_set(): break
        conversation_history.append(HumanMessage(content=user_txt))

    conv_history = get_buffer_string(conversation_history)
    # run the onboarding_agent *only* if the loop reached a natural end
    if not stop_event.is_set():
        template = "Save the data of the following user: {}"
        asyncio.run(
            run_agent(
                agent=onboarding_agent,
                task_template=template,
                message_source="onboarding_agent",
                input_text=conv_history
            )
        )
    thread_alive.set()
    # enable Start again
    root.after(0, lambda: (start_btn.config(state=tk.NORMAL),
                           stop_btn.config(state=tk.DISABLED)))

# ----------------------  button handlers -------------------------------
def on_start():
    stop_event.clear(); thread_alive.clear()
    start_btn.config(state=tk.DISABLED); stop_btn.config(state=tk.NORMAL)
    threading.Thread(target=conversational_loop, daemon=True).start()

def on_stop():
    stop_event.set()            # ask the loop to quit
    if not thread_alive.wait(timeout=5):   # wait up to 5 s
        print("Forced stop.")
    start_btn.config(state=tk.NORMAL); stop_btn.config(state=tk.DISABLED)
    msg_lbl.config(text="Conversation aborted.")

def on_close():
    stop_event.set()
    root.destroy()

start_btn.config(command=on_start)
stop_btn .config(command=on_stop)
root.protocol("WM_DELETE_WINDOW", on_close)

root.mainloop()

# -------------------------  after GUI exits  ----------------------------
if conv_history:
    print(" Conversation History ".center(30, "-"))
    print(conv_history)