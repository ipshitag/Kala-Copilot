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
    campaign_generation_tool,
    add_users_to_cosmos,
    add_product_to_cosmos
)
from bing_search_tool import estimate_art_price_range

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

deployment_name = os.environ.get("AZURE_OPENAI_DEPLOYMENT")
project_connection_string = os.getenv("AZURE_AI_FOUNDRY_CONNECTION_STRING")

# Create the project client
project_client = AIProjectClient.from_connection_string(
    conn_str=project_connection_string, credential=DefaultAzureCredential())

file_path = r"src/tools/prompts/PricingAgentPrompt.txt"
file_path = Path(file_path)

with file_path.open("r", encoding="utf-8", errors="ignore") as file:
            instructions = file.read()

pricing_functions_tool = FunctionTool(
    {
        add_product_to_cosmos
    }
)

pricing_functions_toolset = ToolSet()
pricing_functions_toolset.add(pricing_functions_tool)

agent = project_client.agents.create_agent(
            model=deployment_name,
            name="Pricing Agent",
            instructions=instructions,
            toolset=pricing_functions_toolset,
            temperature=0.5,
            headers={"x-ms-enable-preview": "true"},
        )