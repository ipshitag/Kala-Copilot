import base64
from mimetypes import guess_type
import os  
import json
import re
import base64
from openai import AzureOpenAI  
from dotenv import load_dotenv
load_dotenv()

azure_deployment = os.environ.get("AZURE_OPENAI_DEPLOYMENT")
api_version = os.environ.get("AZURE_OPENAI_API_VERSION")
azure_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
api_key = os.environ.get("AZURE_OPENAI_KEY")

az_model_client = AzureOpenAI(
    azure_deployment=azure_deployment,
    api_version=api_version,
    azure_endpoint=azure_endpoint,
    api_key=api_key,
)

def image_describing_tool(image_input, additional_instruction= None, mime_type=None):
    """ Accepts either a file path (str) or bytes object for the image.
    Optionally, provide mime_type (required for bytes; guessed for path).
    Returns structured craft info as dict if successful, else str with error message.
    """
    # Step 1: Load and encode image
    try:
        if isinstance(image_input, str):  # File path
            if not os.path.isfile(image_input):
                return f"Error: File '{image_input}' does not exist. Please check your path."
            if mime_type is None:
                mime_type, _ = guess_type(image_input)
            with open(image_input, "rb") as image_file:
                image_bytes = image_file.read()
            if len(image_bytes) == 0:
                return f"Error: File '{image_input}' is empty."
        elif isinstance(image_input, bytes):
            image_bytes = image_input
            if not image_bytes:
                return "Error: Provided image bytes are empty."
        else:
            return "Error: image_input must be a file path (str) or bytes object."
    except Exception as e:
        return f"Error reading image: {str(e)}"

    if mime_type is None:
        mime_type = 'application/octet-stream'

    try:
        base64_encoded_data = base64.b64encode(image_bytes).decode('utf-8')
    except Exception as e:
        return f"Error: failed to base64-encode image ({str(e)})."

    # Step 2: Construct chat prompt
    if additional_instruction:
        prompt = """Please look at the image and provide a detailed description in the following format:
                    [JSON START]
                    {
                        "description": "A detailed description of the image",
                        "craft": "The name of the craft (in english for the masses)",
                        "traditional_name": "The traditional name of the craft eg Sohrai, Pattachitra, Warli, Kalamkari, etc.",
                        "location": "The location where the craft is made",
                        "cultural_significance": "The cultural significance of the piece"
                        "size": "The size of the piece",
                        "material": "The material used in the piece",
                    }
                    [JSON END]
                    
                    Additional instruction: {}
                    """.format(additional_instruction=additional_instruction)
    else:
        prompt = """Please look at the image and provide a detailed description in the following format:
                    [JSON START]
                    {
                        "description": "A detailed description of the image",
                        "craft": "The name of the craft (in english for the masses)",
                        "traditional_name": "The traditional name of the craft eg Sohrai, Pattachitra, Warli, Kalamkari, etc.",
                        "location": "The location where the craft is made",
                        "cultural_significance": "The cultural significance of the piece"
                        "size": "The size of the piece",
                        "material": "The material used in the piece",
                    }
                    [JSON END]
                    """
    chat_prompt = [
        {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": """You are an AI assistant whose task is to describe image as required by the user. <...your full prompt here...>"""
                }
            ]
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": """""".format(prompt)
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:{mime_type};base64,{base64_encoded_data}"
                    }
                },
            ]
        }
    ]

    # Step 3: Model call with error handling
    try:
        completion = az_model_client.chat.completions.create(
            model="gpt-4o",
            messages=chat_prompt,
            max_tokens=800,
            temperature=0.7,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None,
            stream=False
        )
    except Exception as e:
        return f"Error: Model call failed ({str(e)}). Check network connection and credentials."

    try:
        response_dict = completion.model_dump()
        response_message = response_dict["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: Unexpected model response structure ({str(e)})."

    # Step 4: Extract and parse JSON from response
    match = re.search(r'\{.*\}', response_message, re.DOTALL)
    if not match:
        return "Error: Model response does not contain a JSON block in the expected format."
    json_str = match.group(0)
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        return f"Error: Failed to parse JSON from model response ({str(e)}). Model output was:\n{json_str}"
    except Exception as e:
        return f"Error: Unknown error parsing JSON: {str(e)}"
    
    return data

def campaign_generation_tool(information):
    information = str(information)
    output = "Given the following information, please create a campaign for the product. The information is as follows:\n{}".format(information)
    chat_prompt = [
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": """You are an AI assistant whose task is to create amazing campaigns for the given information. You are adept in Indian traditional handicrafts and can provide detailed descriptions of the images. You are also capable of providing information about the craft, and the cultural significance of the piece. The campaign is to sell stuff."""
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """{output}

                        Please provide the campaign in the following format:
                        [JSON START]
                        {{
                            "campaign_name": "The name of the campaign",
                            "description": "A detailed description of the campaign",
                            "target_audience": "The target audience for the campaign",
                            "platforms": "The platforms where the campaign will be run",
                            "budget": "The budget for the campaign",
                            "duration": "The duration of the campaign",
                            "goals": "The goals of the campaign"
                        }}
                        [JSON END]
                        """.format(output=output)
                    },

    ]},
                ]


    messages = chat_prompt 

    completion = az_model_client.chat.completions.create(  
        model="gpt-4o",  
        messages=messages,
        max_tokens=800,  
        temperature=0.7,  
        top_p=0.95,  
        frequency_penalty=0,  
        presence_penalty=0,
        stop=None,  
        stream=False  
    )  
    response_dict = completion.model_dump()
    response_message = response_dict["choices"][0]["message"]["content"]
    match = re.search(r'\{.*\}', response_message, re.DOTALL)
    if match:
        json_str = match.group(0)
        # Step 2: Load as dict
        data = json.loads(json_str)
        return (data)
    else:
        return ("No JSON found") 
