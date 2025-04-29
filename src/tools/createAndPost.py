import os
from requests_oauthlib import OAuth1Session
from dotenv import load_dotenv
from azure.cosmos import CosmosClient, exceptions
from openai import AzureOpenAI
import json
import base64
import requests 

# Load environment variables from .env file
load_dotenv()



# Twitter API credentials
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")

# Cosmos DB credentials
COSMOS_ENDPOINT = os.getenv("COSMOS_DB_ENDPOINT")
COSMOS_KEY = os.getenv("COSMOS_DB_KEY")
DATABASE_NAME = os.getenv("DATABASE_NAME")
CONTAINER_NAME = os.getenv("CONTAINER_NAME")

# Azure OpenAI credentials
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")

def generate_marketing_post(product_data: str, image_path=None):
    """
    Generate a marketing post using Azure OpenAI.
    """
    try:
        # Extract all relevant product data fields
        product_name = product_data.get("productName", "Unknown Product")
        product_description = product_data.get("productDescription", "No description available.")
        marketing_copy = product_data.get("marketingCopy", "No marketing copy available.")
        price = product_data.get("price", "N/A")
        category = product_data.get("category", "Uncategorized")
        image_url = product_data.get("imageUrl", None)

        # If image_url is provided, download the image
        if image_url and not image_path:
            response = requests.get(image_url)
            if response.status_code == 200:
                image_path = "temp_image.jpg"
                with open(image_path, "wb") as image_file:
                    image_file.write(response.content)
                print(f"✅ Image downloaded successfully from URL: {image_url}")
            else:
                print(f"❌ Failed to download image from URL: {image_url}. Status code: {response.status_code}")

        PROMPT = """
You are an agent responsible for crafting social media posts that highlight local artisans and their creations. For each product, you will draft an engaging and informative post suitable for **Twitter** (maximum 280 characters). The goal is to captivate potential buyers by sharing the story behind the product, its craftsmanship, and its cultural significance.

### **Instructions:**

1. **Analyze the Product Data**:
   - Use the **product name**, **description**, **marketing copy**, **price** and any relevant details to highlight the uniqueness and craftsmanship of the item. Prices are in dollars.
   - Emphasize **cultural heritage**, **traditional craftsmanship**, and the **story** behind the product.
   - Keep the tone **engaging**, **informal**, and **inspirational** to make the audience feel connected to the artisan's work.

2. **Focus on Key Elements**:
   - Mention any **visual features** or **cultural significance** in the product description.
   - Include **relevant details** from the product description, like its historical or cultural roots, and how it reflects the artisan's craftsmanship.
   - Use **short, catchy phrases** and **hashtags** that resonate with those interested in unique, handmade products, traditional crafts, or local heritage.

3. **Structure of the Post**:
   - **Introduction**: A short, compelling statement that grabs attention.
   - **Middle**: A brief mention of the key features (product description) and what makes the piece unique.
   - **Closing**: A call-to-action or invitation to learn more/purchase the item.
   - Use **hashtags** like #HandmadeArt, #TraditionalCraft, #ArtisansOfInstagram, #LocalCrafts, or specific ones related to the craft.

4. **Example Output**:
   - **For an Art Piece (like a painting)**: 
     "Experience the timeless beauty of [Product Name] 🎨✨. Crafted with love, this [Craft Type] captures the essence of [cultural reference]. A true testament to tradition and artistry. Bring a piece of heritage into your home today! #TraditionalCraft #HandmadeArt"
   
   - **For a Piece of Jewelry**: 
     "Shine bright with handmade [Product Name] 💎✨! Each piece tells the story of [artisan/tribe] craftsmanship, blending tradition with beauty. Perfect for those who love meaningful, unique jewelry. #HandcraftedJewelry #ArtisanCraft"

5. **Hashtags**: 
   - Use relevant hashtags based on the craft type, such as #WarliArt, #HandmadeJewelry, #Pottery, #Ceramics, #Woodwork, etc.

### PRODUCT DATA:
{product_data}

## NOTE:
- Make the post **engaging** and **informative** and describe the product in a way that resonates with potential buyers.
- Ensure the post is **within 200 characters** for Twitter.

### **Example Output** (for Twitter):
"Step into the vibrant world of Warli art 🌿✨! This authentic painting from Maharashtra captures the essence of community life in stunning white-on-brown. A grand tree, joyful dances, and nature’s embrace all in one frame. Bring heritage to your home today! #WarliArt #TraditionalCraft"
"""
        
        # Format the product data into a string for the prompt
        prompt_with_data = PROMPT.format(product_data=json.dumps({
            "productName": product_name,
            "productDescription": product_description,
            "marketingCopy": marketing_copy,
            "price": price,
            "category": category,
            "imageUrl": image_url
        }))

        # Initialize the Azure OpenAI client
        azure_openai_client = AzureOpenAI(
            azure_endpoint=AZURE_OPENAI_ENDPOINT, 
            api_key=AZURE_OPENAI_KEY,
            api_version=AZURE_OPENAI_API_VERSION
        )

        # Prepare the message for the OpenAI model
        message = [{"role": "user", "content": prompt_with_data}]

        if image_path:
            with open(image_path, "rb") as image_file:
                image_data = base64.b64encode(image_file.read()).decode('utf-8')
                user_content = [{"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}]
                message.append({"role": "user", "content": user_content})

        # Request completion from the OpenAI model
        response = azure_openai_client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=message,
        )
        print("✅ Marketing post generated successfully.")
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        print(f"❌ Error generating marketing post: {e}")
        return None


def post_tweet_with_product(product_id: str) -> str:
    """
    Fetch product data from Cosmos DB, generate a marketing post, and post it to Twitter.
    
    Args:
        product_id (str): Product id of the product to be posted.
        
    Returns:
        str: Status result of the tweet posting.
    """
    try:
        # Initialize Cosmos DB client
        cosmos_client = CosmosClient(COSMOS_ENDPOINT, credential=COSMOS_KEY)
        database = cosmos_client.get_database_client(DATABASE_NAME)
        container = database.get_container_client(CONTAINER_NAME)

        # Fetch product data from Cosmos DB
        product_data = container.read_item(item=product_id, partition_key=product_id)
        print(product_data)
        print(f"✅ Product data retrieved successfully for Product ID: {product_id}")
    except exceptions.CosmosResourceNotFoundError:
        print(f"❌ Product with ID {product_id} not found in Cosmos DB.")
        return
    except Exception as e:
        print(f"❌ Error retrieving product data: {e}")
        return

    # Generate marketing post using Azure OpenAI
    tweet_text = generate_marketing_post(product_data)
    if not tweet_text:
        print("❌ Failed to generate tweet text. Aborting.")
        return

    # Initialize Twitter OAuth session
    twitter = OAuth1Session(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)

    # Handle media upload if an image URL is provided
    product_image_url = product_data.get("imageUrl", None)
    media_id = None
    if product_image_url:
        try:
            # Download the image from the URL
            response = requests.get(product_image_url)
            if response.status_code == 200:
                image_path = "temp_image.jpg"
                with open(image_path, "wb") as image_file:
                    image_file.write(response.content)
                print(f"✅ Image downloaded successfully from URL: {product_image_url}")

                # Process the downloaded image for media upload
                with open(image_path, "rb") as image_file:
                    files = {"media": image_file}
                    upload_url = "https://upload.twitter.com/1.1/media/upload.json"
                    media_response = twitter.post(upload_url, files=files)

                if media_response.status_code == 200:
                    media_data = media_response.json()
                    media_id = media_data["media_id_string"]
                    print(f"✅ Image uploaded successfully. Media ID: {media_id}")
                else:
                    print(f"❌ Media upload failed. Response: {media_response.text}")
            else:
                print(f"❌ Failed to download image from URL: {product_image_url}. Status code: {response.status_code}")
        except Exception as e:
            print(f"❌ Error handling image: {e}")

    # Prepare the tweet payload
    tweet_payload = {"text": tweet_text}
    if media_id:
        tweet_payload["media"] = {"media_ids": [media_id]}

    # Post the tweet
    try:
        print(f"📢 Posting tweet: {tweet_text}")
        response = twitter.post(
            "https://api.twitter.com/2/tweets",
            json=tweet_payload
        )
        if response.status_code == 201:
            print("✅ Tweet posted successfully!")
        else:
            print(f"❌ Failed to post tweet. Status code: {response.status_code}. Response: {response.text}")
    except Exception as e:
        print(f"❌ Error posting tweet: {e}")

# # Example usage
# if __name__ == "__main__":
#     product_id = "612ddf36-0207-4bd4-9d0a-18e5644de47f"  # Replace with the actual product ID
#     post_tweet_with_product(product_id)