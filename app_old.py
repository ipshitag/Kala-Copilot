import os
import io
import asyncio
from uuid import uuid4
import requests
from flask import Flask, request, session, redirect, url_for, render_template_string
from src.tools.azure_agent_wrapper import branding_agent, cataloger_agent, onboarding_agent, visual_insight_agent, seo_agent, user_proxy, planning_agent, selector_prompt
from src.tools.agent_tools import image_describing_tool
from PIL import Image

# ---- BEGIN: Azure Blob Storage Setup ----
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
# ---- END: Azure Blob Storage Setup ----

async def run_agent(agent, task_template, message_source, input_text):
    task = task_template.format(input_text)
    result = await agent.run(task=task)
    for msg in result.messages:
        if getattr(msg, "source", None) == message_source:
            return msg.content
    return result.messages[-1].content

app = Flask(__name__)
app.secret_key = "some_secret_key_for_demo"

@app.route("/")
def index():
    html = """
    <h1>Welcome to the Step-by-Step WebApp</h1>
    <ol>
        <li><a href='/upload'>Upload Image (Step 0)</a></li>
    </ol>
    """
    return render_template_string(html)

# STEP 0: Upload image to Azure Blob and store URL
@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        uploaded_file = request.files.get("image_file")
        if not uploaded_file or not uploaded_file.filename:
            html = "<h3>Error: Please select an image file to upload.</h3><a href='/upload'>Try again</a>"
            return render_template_string(html)
        filename = uploaded_file.filename

        # Make filename unique
        ext = ""
        if "." in filename:
            ext = "." + filename.rsplit(".", 1)[1]
        unique_filename = f"{uuid4().hex}{ext}"

        try:
            blob_url = upload_image_to_blob(uploaded_file.stream, unique_filename)
            print("Upload successful. Blob URL:", blob_url)
            session["image_blob_url"] = blob_url
            # Wipe previous downstream steps
            for k in ["image_description", "visual_agent_result", "branding_agent_result", "seo_agent_result", "cataloger_agent_result"]:
                session.pop(k, None)
            return redirect(url_for("step1"))
        except Exception as e:
            import traceback
            traceback.print_exc()
            html = f"<h3>Upload failed: {e}</h3><a href='/upload'>Try again</a>"
            return render_template_string(html)

    html = """
        <h2>Step 0: Upload Image</h2>
        <form method="POST" enctype="multipart/form-data">
            <label>Upload Image (file):</label>
            <input type="file" name="image_file" accept="image/*" /><br><br>
            <button type="submit">Upload Image</button>
        </form>
    """
    return render_template_string(html)

# STEP 1: Use the uploaded blob url for description
@app.route("/step1", methods=["GET", "POST"])
def step1():
    blob_url = session.get("image_blob_url")
    if not blob_url:
        return redirect(url_for("upload"))
    if request.method == "POST":
        description = image_describing_tool(blob_url)
        session["image_description"] = description
        return redirect(url_for("step2"))
    html = f"""
        <h2>Step 1: Image Description</h2>
        <p>Uploaded Image:</p>
        <img src="{blob_url}" style="max-height:200px"/><br><br>
        <form method="POST">
            <button type="submit">Generate Description & Next</button>
        </form>
        <br><a href="/upload">Upload a different image</a>
    """
    return render_template_string(html)

@app.route("/step2", methods=["GET", "POST"])
def step2():
    if "image_description" not in session:
        return redirect(url_for("step1"))
    if request.method == "POST":
        image_description = session["image_description"]
        visual_task = "Create a polished and stunning description of this product: {}"
        visual_agent_result = asyncio.run(
            run_agent(
                agent=visual_insight_agent,
                task_template=visual_task,
                message_source="visual_insight_agent",
                input_text=image_description
            )
        )
        session["visual_agent_result"] = visual_agent_result
        return redirect(url_for("step3"))
    blob_url = session.get("image_blob_url", "")
    html = f"""
        <h2>Step 2: Visual Insight Agent</h2>
        <img src="{blob_url}" style="max-height:150px;"/><br>
        <p><strong>Image Description (from Step 1):</strong> {session["image_description"]}</p>
        <form method="POST">
            <button type="submit">Generate Visual Insight & Next</button>
        </form>
    """
    return render_template_string(html)

@app.route("/step3", methods=["GET", "POST"])
def step3():
    if "visual_agent_result" not in session:
        return redirect(url_for("step2"))
    if request.method == "POST":
        marketing_cmd = "Based on this product description, create a marketing ad copy: {}"
        branding_result = asyncio.run(
            run_agent(
                agent=branding_agent,
                task_template=marketing_cmd,
                message_source="branding_agent",
                input_text=session["visual_agent_result"]
            )
        )
        session["branding_agent_result"] = branding_result
        return redirect(url_for("step4"))
    html = f"""
        <h2>Step 3: Branding Agent</h2>
        <p><strong>Visual Agent Result:</strong> {session["visual_agent_result"]}</p>
        <form method="POST">
            <button type="submit">Generate Marketing Copy & Next</button>
        </form>
    """
    return render_template_string(html)

@app.route("/step4", methods=["GET", "POST"])
def step4():
    if "branding_agent_result" not in session:
        return redirect(url_for("step3"))
    if request.method == "POST":
        seo_cmd = "Create an SEO-optimized product description for the following text: {}"
        seo_result = asyncio.run(
            run_agent(
                agent=seo_agent,
                task_template=seo_cmd,
                message_source="seo_agent",
                input_text=session["branding_agent_result"]
            )
        )
        session["seo_agent_result"] = seo_result
        return redirect(url_for("step5"))
    html = f"""
        <h2>Step 4: SEO Agent</h2>
        <p><strong>Branding Agent Result:</strong> {session["branding_agent_result"]}</p>
        <form method="POST">
            <button type="submit">Generate SEO Copy & Next</button>
        </form>
    """
    return render_template_string(html)

@app.route("/step5", methods=["GET", "POST"])
def step5():
    blob_url = session.get("image_blob_url")
    if "seo_agent_result" not in session:
        return redirect(url_for("step4"))
    if request.method == "POST":
        catalog_cmd = "Create a product catalog entry based on the following copy: {}"
        image_url_add = "\n\nImage URL: " + blob_url
        catalog_cmd = catalog_cmd + image_url_add
        catalog_result = asyncio.run(
            run_agent(
                agent=cataloger_agent,
                task_template=catalog_cmd,
                message_source="cataloger_agent",
                input_text=session["seo_agent_result"]
            )
        )
        session["cataloger_agent_result"] = catalog_result
        return redirect(url_for("final"))
    html = f"""
        <h2>Step 5: Cataloger Agent</h2>
        <p><strong>SEO Agent Result:</strong> {session["seo_agent_result"]}</p>
        <form method="POST">
            <button type="submit">Generate Catalog Entry & Next</button>
        </form>
    """
    return render_template_string(html)

@app.route("/final")
def final():
    if "cataloger_agent_result" not in session:
        return redirect(url_for("step5"))
    blob_url = session.get("image_blob_url", "")
    image_tag = f'<img src="{blob_url}" alt="Uploaded image" style="max-height:150px;"><br>' if blob_url else ""
    html = f"""
    <h2>Final Output</h2>
    {image_tag}
    <p><strong>Image Description (Step 1):</strong> {session.get("image_description", "")}</p>
    <p><strong>Visual Agent Result (Step 2):</strong> {session.get("visual_agent_result", "")}</p>
    <p><strong>Branding Agent Result (Step 3):</strong> {session.get("branding_agent_result", "")}</p>
    <p><strong<p><strong>SEO Agent Result (Step 4):</strong> {session.get("seo_agent_result", "")}</p>
    <p><strong>Cataloger Agent Result (Step 5):</strong> {session.get("cataloger_agent_result", "")}</p>
    <br>
    <a href="/">Go Home</a>
    """
    return render_template_string(html)


if __name__ == "__main__":
    # Run the Flask app
    app.run(debug=True)