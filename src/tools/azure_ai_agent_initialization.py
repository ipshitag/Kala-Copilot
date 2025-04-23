from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import BingGroundingTool, CodeInterpreterTool
import time
from pathlib import Path
import os
from azure.ai.projects.models import FunctionTool, ToolSet, MessageTextContent
from azure.core.exceptions import HttpResponseError
from agent_tools import (
    image_describing_tool,
    campaign_generation_tool
)

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

deployment_name = os.environ.get("AZURE_OPENAI_DEPLOYMENT")
project_connection_string = os.getenv("AZURE_AI_FOUNDRY_CONNECTION_STRING")

# Create the project client
project_client = AIProjectClient.from_connection_string(
    conn_str=project_connection_string, credential=DefaultAzureCredential())

file_path = r"src\tools\prompts\BrandingAgent.txt"
file_path = Path(file_path)

with file_path.open("r", encoding="utf-8", errors="ignore") as file:
            instructions = file.read()

visual_insight_functions_tool = FunctionTool(
    {
        image_describing_tool
    }
)

visual_insight_functions_toolset = ToolSet()
visual_insight_functions_toolset.add(visual_insight_functions_tool)

agent = project_client.agents.create_agent(
            model=deployment_name,
            name="Visual Insights Agent",
            instructions=instructions,
            # toolset=visual_insight_functions_toolset,
            temperature=0.5,
            headers={"x-ms-enable-preview": "true"},
        )