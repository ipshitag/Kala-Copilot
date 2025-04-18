import base64
from mimetypes import guess_type
import os  
import json
import re
import base64
from openai import AzureOpenAI  
from azure.identity import DefaultAzureCredential, get_bearer_token_provider 

api_base = '<your_azure_openai_endpoint>' # your endpoint should look like the following https://YOUR_RESOURCE_NAME.openai.azure.com/
api_key="<your_azure_openai_key>"
deployment_name = '<your_deployment_name>'
api_version = '2024-02-15-preview' # this might change in the future

az_model_client = AzureOpenAI(
    azure_deployment="gpt-4o",
    api_version="2025-01-01-preview",
    azure_endpoint="https://chatgpttest45.openai.azure.com/",
    api_key="50bb20b0bf1b4fb88d1d9ffe65e0ab66",
) 

# Function to encode a local image into data URL 
def image_describing_tool(image_path):
    # Guess the MIME type of the image based on the file extension
    mime_type, _ = guess_type(image_path)
    if mime_type is None:
        mime_type = 'application/octet-stream'  # Default MIME type if none is found

    # Read and encode the image file
    with open(image_path, "rb") as image_file:
        base64_encoded_data = base64.b64encode(image_file.read()).decode('utf-8')

    # Construct the data URL
    image_url =  f"data:{mime_type};base64,{base64_encoded_data}"
    chat_prompt = [
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": """You are an AI assistant whose task is to describe image as required by the user. You are adept in Indian traditional handicrafts and can provide detailed descriptions of the images. You are also capable of providing information about the craft, and the cultural significance of the piece. Quick Visual Guide: Sohrai: Geometric patterns and animal motifs with natural earth tones.
Warli: White stick figures and simple geometric shapes on earthy backgrounds.
Madhubani: Intricate patterns, vibrant colors, and double-line borders.
Pattachitra: Bold colors with mythological narratives and detailed borders.
Tanjore: Rich colors and gold foil with embossed religious figures.
Gond: Vivid colors with detailed lines and dots forming whimsical animals.
Kalamkari: Intricate lines and floral patterns with mythological subjects.
Phad: Narrative panels with vibrant colors and stylized figures.
Rangoli: Decorative floor art with symmetrical patterns using colored powders."""
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """Please look at the image and provide a detailed description in the following format:
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
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_encoded_data}"
                        }
                    },
                ]
            }
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

desc = image_describing_tool(r"C:\Users\v-ighosh\Desktop\work pro\Retail-Copilot-Hackathon\src\tools\image2.jpg")
camp = campaign_generation_tool(desc)
print(camp)