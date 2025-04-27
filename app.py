import os
import asyncio
from uuid import uuid4
import json
from flask import Flask, request, session, render_template, redirect, url_for, jsonify
from PIL import Image

# Import your custom modules
from src.tools.azure_agent_wrapper import (
    branding_agent,
    cataloger_agent,
    onboarding_agent,
    visual_insight_agent,
    seo_agent,
    user_proxy,
    planning_agent,
    selector_prompt,
)
from src.tools.agent_tools import image_describing_tool

# ---- Azure Blob Storage Setup ----
from azure.storage.blob import BlobServiceClient

AZURE_BLOB_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
AZURE_BLOB_CONTAINER_NAME = os.getenv("AZURE_CONTAINER_NAME")

blob_service_client = BlobServiceClient.from_connection_string(AZURE_BLOB_CONNECTION_STRING)
container_client = blob_service_client.get_container_client(AZURE_BLOB_CONTAINER_NAME)

def upload_image_to_blob(file_obj, filename):
    blob_client = container_client.get_blob_client(filename)
    file_obj.seek(0)
    blob_client.upload_blob(file_obj, overwrite=True)
    blob_url = blob_client.url
    return blob_url

# ---- Flask App ----
app = Flask(__name__)
app.secret_key = "some_secret_key_for_demo"

async def run_agent(agent, task_template, message_source, input_text):
    task = task_template.format(input_text)
    result = await agent.run(task=task)
    for msg in result.messages:
        if getattr(msg, "source", None) == message_source:
            return msg.content
    return result.messages[-1].content

# -------------------------------
# INDEX
# -------------------------------
@app.route("/")
def index():
    return render_template("index.html")

# -------------------------------
# STEP 0: UPLOAD
# -------------------------------
@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        uploaded_file = request.files.get("image_file")
        if not uploaded_file or not uploaded_file.filename:
            return render_template("upload.html", error="Please select an image file to upload.")
        filename = uploaded_file.filename
        extension = ""
        if "." in filename:
            extension = "." + filename.rsplit(".", 1)[1]
        unique_filename = f"{uuid4().hex}{extension}"
        try:
            blob_url = upload_image_to_blob(uploaded_file.stream, unique_filename)
            session["image_blob_url"] = blob_url
            for k in [
                "image_description",
                "visual_agent_result",
                "branding_agent_result",
                "seo_agent_result",
                "cataloger_agent_result",
            ]:
                session.pop(k, None)
            return redirect(url_for("step1"))
        except Exception as e:
            return render_template("upload.html", error=str(e))
    return render_template("upload.html")

# -------------------------------
# STEP 1: IMAGE DESCRIPTION
# -------------------------------
@app.route("/step1", methods=["GET"])
def step1():
    blob_url = session.get("image_blob_url")
    if not blob_url:
        return redirect(url_for("upload"))
    return render_template("step1.html", blob_url=blob_url)

@app.route("/generate_description", methods=["POST"])
def generate_description():
    data = request.get_json()
    blob_url = data.get("imageUrl")
    if not blob_url:
        return jsonify({"error": "No image URL provided."}), 400
    feedback = data.get("feedback", "")  # Capture additional feedback if provided
    # Assuming image_describing_tool can optionally take feedback
    try:
        description = image_describing_tool(blob_url, feedback=feedback)
        description = json.dumps(description)
        session["image_description"] = description
        # Optionally store feedback in session for use in subsequent steps
        if feedback:
            session["additional_feedback"] = feedback
        return jsonify({"description": description})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -------------------------------
# STEP 2: VISUAL INSIGHT AGENT
# -------------------------------
@app.route("/step2", methods=["GET"])
def step2():
    blob_url = session.get("blob_url", "")
    image_description = session.get("image_description", "")
    if not image_description:
        # If no description found, redirect back so user can generate it
        return redirect(url_for("step1"))
    return render_template("step2.html", blob_url=blob_url, image_description=image_description)

@app.route("/generate_insight", methods=["POST"])
def generate_insight():
    data = request.get_json()
    image_description = session.get("image_description")
    feedback = session.get("feedback", "")  # Capture additional feedback if provided

    if not image_description:
        return jsonify({"error": "No image description found in session."}), 400
    
    try:
        prompt_template = "Create a polished and stunning description of this product: {}"
        if feedback:  # Use feedback if provided
            prompt_template += f"\n\nAdditional Feedback: {feedback}"
        visual_agent_result = asyncio.run(
            run_agent(
                agent=visual_insight_agent,
                task_template=prompt_template,
                message_source="visual_insight_agent",
                input_text=image_description
            )
        )
        # Save result in session if you want to use it in subsequent steps
        session["visual_agent_result"] = visual_agent_result

        return jsonify({"visual_insight": visual_agent_result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -------------------------------
# STEP 3: BRANDING AGENT
# -------------------------------
@app.route("/step3", methods=["GET"])
def step3():
    if "visual_agent_result" not in session:
        return redirect(url_for("step2"))
    return render_template(
        "step3.html",
        visual_agent_result=session["visual_agent_result"]
    )

@app.route("/generate_branding", methods=["POST"])
def generate_branding():
    visual_result = session.get("visual_agent_result")
    data = request.get_json()
    feedback = data.get("feedback", "")
    is_feedback = data.get("isFeedback", False)  # Indicator if this is a feedback regeneration or not
    if not visual_result:
        return jsonify({"error": "No visual agent result found in session."}), 400
    try:
        marketing_cmd = "Based on this product description, create a marketing ad copy: {}"
        if is_feedback and feedback:  # Modify text based on if feedback is present and this is a regeneration
            marketing_cmd += f"\n\nFeedback: {feedback}"
        branding_result = asyncio.run(
            run_agent(
                agent=branding_agent,
                task_template=marketing_cmd,
                message_source="branding_agent",
                input_text=visual_result
            )
        )
        session["branding_agent_result"] = branding_result
        return jsonify({"branding_copy": branding_result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -------------------------------
# STEP 4: SEO AGENT
# -------------------------------
@app.route("/step4", methods=["GET"])
def step4():
    if "branding_agent_result" not in session:
        return redirect(url_for("step3"))
    return render_template(
        "step4.html",
        branding_result=session["branding_agent_result"]
    )

@app.route("/generate_seo", methods=["POST"])
def generate_seo():
    branding_res = session.get("branding_agent_result")
    data = request.get_json()
    feedback = data.get("feedback", "")  # Now accepting feedback
    if not branding_res:
        return jsonify({"error": "No branding result in session."}), 400
    try:
        seo_cmd = "Create an SEO-optimized product description for the following text: {}"
        if feedback:  # If there's feedback, include it
            seo_cmd += f"\n\nFeedback: {feedback}"
        seo_result = asyncio.run(
            run_agent(
                agent=seo_agent,
                task_template=seo_cmd,
                message_source="seo_agent",
                input_text=branding_res
            )
        )
        session["seo_agent_result"] = seo_result
        return jsonify({"seo_copy": seo_result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -------------------------------
# STEP 5: CATALOGER AGENT
# -------------------------------
@app.route("/step5", methods=["GET"])
def step5():
    if "seo_agent_result" not in session:
        return redirect(url_for("step4"))
    return render_template(
        "step5.html",
        seo_result=session["seo_agent_result"]
    )

@app.route("/generate_catalog", methods=["POST"])
def generate_catalog():
    seo_res = session.get("seo_agent_result")
    data = request.get_json()
    feedback = data.get("feedback", "")  # Capture additional feedback from the request
    blob_url = session.get("image_blob_url", "")
    if not seo_res:
        return jsonify({"error": "No SEO result in session."}), 400
    try:
        catalog_cmd = "Create a product catalog entry based on the following copy: {}"
        if feedback:  # Add feedback to the command if present
            catalog_cmd += f"\n\nFeedback: {feedback}"
        catalog_cmd = catalog_cmd + f"\n\nImage URL: {blob_url}"
        catalog_result = asyncio.run(
            run_agent(
                agent=cataloger_agent,
                task_template=catalog_cmd,
                message_source="catalog_entry",
                input_text=seo_res
            )
        )
        session["cataloger_agent_result"] = catalog_result
        return jsonify({"catalog_entry": catalog_result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -------------------------------
# FINAL: SHOW ALL OUTPUTS
# -------------------------------
@app.route("/final", methods=["GET"])
def final():
    if "cataloger_agent_result" not in session:
        return redirect(url_for("step5"))
    blob_url = session.get("image_blob_url", "")
    return render_template(
        "final.html",
        blob_url=blob_url,
        image_description=session.get("image_description", ""),
        visual_agent_result=session.get("visual_agent_result", ""),
        branding_agent_result=session.get("branding_agent_result", ""),
        seo_agent_result=session.get("seo_agent_result", ""),
        cataloger_agent_result=session.get("cataloger_agent_result", "")
    )

if __name__ == "__main__":
    app.run(debug=True)