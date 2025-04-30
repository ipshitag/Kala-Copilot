import base64
from mimetypes import guess_type
import os  
import json
from azure.cosmos import CosmosClient, exceptions
import uuid
from datetime import datetime
import requests
import re
import base64
from openai import AzureOpenAI  
from dotenv import load_dotenv
load_dotenv()

azure_deployment = os.environ.get("AZURE_OPENAI_DEPLOYMENT")
api_version = os.environ.get("AZURE_OPENAI_API_VERSION")
azure_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
api_key = os.environ.get("AZURE_OPENAI_KEY")
cc_endpoint = os.environ.get("COSMOS_DB_ENDPOINT") 
cc_key = os.environ.get("COSMOS_DB_KEY") 
cc_client = CosmosClient(cc_endpoint, cc_key)
# Define database and container names
cc_database_name = "retail-copilot"
# Cosmos DB credentials
COSMOS_ENDPOINT = os.getenv("COSMOS_DB_ENDPOINT")
COSMOS_KEY = os.getenv("COSMOS_DB_KEY")
DATABASE_NAME = os.getenv("DATABASE_NAME")
CONTAINER_NAME = "users"

az_model_client = AzureOpenAI(
    azure_deployment="gpt-4o",
    api_version=api_version,
    azure_endpoint=azure_endpoint,
    api_key=api_key,
)


def image_describing_tool(image_input, feedback = None, mime_type=None):
    ...

    try:
        if isinstance(image_input, str):
            if image_input.startswith("http://") or image_input.startswith("https://"):
                # For HTTP(S) image URL: Use URL directly
                image_mode = "url"
                image_url = image_input
                if mime_type is None:
                    # Guess mime_type (optional)
                    mime_type, _ = guess_type(image_input)
            else:
                # Local file path
                if not os.path.isfile(image_input):
                    return f"Error: File '{image_input}' does not exist. Please check the path."
                if mime_type is None:
                    mime_type, _ = guess_type(image_input)
                with open(image_input, "rb") as image_file:
                    image_bytes = image_file.read()
                    if len(image_bytes) == 0:
                        return f"Error: File '{image_input}' is empty."
                image_mode = "bytes"
        elif isinstance(image_input, bytes):
            if not image_input:
                return "Error: Provided image bytes are empty."
            image_bytes = image_input
            image_mode = "bytes"
        else:
            return "Error: image_input must be a URL, file path (str), or bytes object."
    except Exception as e:
        return f"Error reading image: {str(e)}"

    # ----------------------------
    # Construct chat prompt
    common_prompt = "Please look at the image and provide a detailed description to the last minute details. Include details like traditional_name, size, color, and material used in the image. Give an appropriate size of the object in image (use your best guess) Provide in a crude way, which will be polished later. If the is not a product, please say so. If its some scenery, or some docvument, just say so."

    if feedback:
        common_prompt += f"\nThe feedback from user is: {feedback}"

    chat_prompt = [
        {
            "role": "system",
            "content": "You are an AI assistant whose task is to describe the image as required by the user."
        }
    ]

    if image_mode == "url":
        # HTTP image: use image URL
        chat_prompt.append({
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": common_prompt
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": image_url
                    }
                }
            ]
        })
    else:
        # Local file or bytes, use data URL (base64)
        if mime_type is None:
            mime_type = "application/octet-stream"
        try:
            base64_encoded_data = base64.b64encode(image_bytes).decode('utf-8')
        except Exception as e:
            return f"Error: failed to base64-encode image ({str(e)})."
        chat_prompt.append({
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": common_prompt
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:{mime_type};base64,{base64_encoded_data}"
                    }
                }
            ]
        })

    # Step 3: Model call with error handling
    try:
        completion = az_model_client.chat.completions.create(
            model="gpt-4o",
            messages=chat_prompt,
            max_tokens=1200,
            temperature=0.7,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None,
            stream=False
        )
    except Exception as e:
        return f"Error: Model call failed ({str(e)}). Check network connection and credentials."

    response_dict = completion.model_dump()
    response_message = response_dict["choices"][0]["message"]["content"]
    
    return response_message

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

def add_product_to_cosmos(
    product_name: str,
    user_id:str,
    product_description: str,
    price: float,
    category: str,
    marketing_copy: str,
    image_url: str = None,
) -> str:
    """
    Add a product with all necessary fields to Cosmos DB.

    Parameters:
    - product_name (str): Product title.
    - user_id (str): User ID of the person adding the product.
    - product_description (str): Details of the product.
    - price (float): Product price.
    - category (str): Product category or type.
    - marketing_copy (str): Short, promotional copy.

    Returns:
    - str: JSON string with product ID and confirmation message.
    """
    # Generate a unique product ID
    product_id = str(uuid.uuid4())

    cc_container_name = "marketing-copy"
    database = cc_client.get_database_client(cc_database_name)
    container = database.get_container_client(cc_container_name)

    item = {
        "id": product_id,
        "productName": product_name,
        "user_id": user_id,
        "productDescription": product_description,
        "price": price,
        "category": category,
        "marketingCopy": marketing_copy,
        "imageUrl": image_url,
    }

    container.create_item(body=item)
    return json.dumps({
        "productID": product_id,
        "message": "Product successfully added!"
    })

def add_users_to_cosmos(
    user_name: str,
    user_forte: str,
    user_id: str,
) -> str:
    
    cc_container_name = "users"
    database = cc_client.get_database_client(cc_database_name)
    container = database.get_container_client(cc_container_name)

    item = {
        "id": user_id,
        "userName": user_name,
        "userForte": user_forte,
    }

    container.create_item(body=item)
    return json.dumps({
        "userID": user_id,
        "message": "Product successfully added!"
    })

def fetch_user_data(user_id: str) -> dict:
    cosmos_client = CosmosClient(COSMOS_ENDPOINT, credential=COSMOS_KEY)
    database = cosmos_client.get_database_client(DATABASE_NAME)
    container = database.get_container_client(CONTAINER_NAME)

    # Fetch product data from Cosmos DB
    user_data = container.read_item(item=user_id, partition_key=user_id)
    user_name = user_data.get("userName")
    userForte = user_data.get("userForte", "No description available.")
    res = "User Name: {}, User Forte: {}".format(user_name, userForte)
    return res


# path = "https://staidemodev.blob.core.windows.net/retail-copilot/image1.jpg"
# res = image_describing_tool(path)
# print(res)