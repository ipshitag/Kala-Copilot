import os
import io
import asyncio
import requests
from flask import Flask, request, session, redirect, url_for, render_template_string
from src.tools.azure_agent_wrapper import branding_agent, cataloger_agent, onboarding_agent,visual_insight_agent,seo_agent,user_proxy,planning_agent,selector_prompt
from src.tools.agent_tools import image_describing_tool
from PIL import Image


# -------------------------------------------------------------------
# ASYNC RUNNER FOR EACH AGENT
# -------------------------------------------------------------------
async def run_agent(agent, task_template, message_source, input_text):
    """
    This function formats the task, calls the agent asynchronously,
    then searches messages for one with the specified 'message_source'.
    """
    task = task_template.format(input_text)
    result = await agent.run(task=task)
    for msg in result.messages:
        if getattr(msg, "source", None) == message_source:
            return msg.content
    return result.messages[-1].content

# -------------------------------------------------------------------
# FLASK APP SETUP
# -------------------------------------------------------------------
app = Flask(__name__)
app.secret_key = "some_secret_key_for_demo"


@app.route("/")
def index():
    """
    Landing page.
    """
    html = """
    <h1>Welcome to the Step-by-Step WebApp</h1>
    <p>• This demo calls image_describing_tool exactly once in Step 1,<br>
       then passes along the text to each agent step via Flask session.</p>
    <a href="/step1">Go to Step 1</a>
    """
    return render_template_string(html)


@app.route("/step1", methods=["GET", "POST"])
def step1():
    """
    Step 1: Prompt the user for an image path or URL, call image_describing_tool (ONE TIME),
    store result in session, and proceed.
    """
    if request.method == "POST":
        file_path_or_url = request.form.get("image_path", "")
        description = image_describing_tool(file_path_or_url)  # <-- Called only once here
        session["image_description"] = description
        return redirect(url_for("step2"))
    else:
        html = """
        <h2>Step 1: Image Description</h2>
        <form method="POST">
            <label for="image_path">Image Path or URL:</label>
            <input type="text" name="image_path" placeholder="http://..." />
            <button type="submit">Describe Image & Next</button>
        </form>
        """
        return render_template_string(html)


@app.route("/step2", methods=["GET", "POST"])
def step2():
    """
    Step 2: Use the stored session image_description to call the visual_insight_agent.
    """
    if "image_description" not in session:
        return redirect(url_for("step1"))  # Ensure user did step1 first

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
    else:
        html = f"""
        <h2>Step 2: Visual Insight Agent</h2>
        <p><strong>Image Description (from Step 1):</strong> {session["image_description"]}</p>
        <form method="POST">
            <button type="submit">Generate Visual Insight & Next</button>
        </form>
        """
        return render_template_string(html)


@app.route("/step3", methods=["GET", "POST"])
def step3():
    """
    Step 3: Use the result from Step 2 to call the branding_agent.
    """
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
    else:
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
    """
    Step 4: Use the result from Step 3 to call the SEO agent.
    """
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
    else:
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
    """
    Step 5: Use the result from Step 4 to call the cataloger_agent.
    """
    if "seo_agent_result" not in session:
        return redirect(url_for("step4"))

    if request.method == "POST":
        catalog_cmd = "Create a product catalog entry based on the following copy: {}"
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
    else:
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
    """
    Final page showing results from all steps. 
    """
    if "cataloger_agent_result" not in session:
        return redirect(url_for("step5"))

    html = f"""
    <h2>Final Output</h2>
    <p><strong>Image Description (Step 1):</strong> {session.get("image_description", "")}</p>
    <p><strong>Visual Agent Result (Step 2):</strong> {session.get("visual_agent_result", "")}</p>
    <p><strong>Branding Agent Result (Step 3):</strong> {session.get("branding_agent_result", "")}</p>
    <p><strong>SEO Agent Result (Step 4):</strong> {session.get("seo_agent_result", "")}</p>
    <p><strong>Cataloger Agent Result (Step 5):</strong> {session.get("cataloger_agent_result", "")}</p>
    <br>
    <a href="/">Go Home</a>
    """
    return render_template_string(html)


if __name__ == "__main__":
    # Run the Flask app
    app.run(debug=True)