import os
import uuid
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load Azure configuration
AZURE_STORAGE_CONNECTION_STRING = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
AZURE_CONTAINER_NAME = os.environ.get("AZURE_CONTAINER_NAME")

if not AZURE_STORAGE_CONNECTION_STRING or not AZURE_CONTAINER_NAME:
    raise ValueError("Azure storage configuration is missing")

blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
container_client = blob_service_client.get_container_client(AZURE_CONTAINER_NAME)

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can specify a list of domains here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve index.html at root
@app.get("/", response_class=FileResponse)
async def serve_index():
    return FileResponse("static/index.html")

# Serve static files (like index.html, CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Handle image uploads
@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    try:
        ext = os.path.splitext(file.filename)[-1]
        blob_name = f"{uuid.uuid4().hex}{ext}"

        contents = await file.read()
        container_client.upload_blob(name=blob_name, data=contents)

        blob_url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{AZURE_CONTAINER_NAME}/{blob_name}"
        return {"blob_url": blob_url, "blob_name": blob_name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
