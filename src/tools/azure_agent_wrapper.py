from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import BingGroundingTool, CodeInterpreterTool
from agent_toolset import visual_insight_functions_toolset
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken
import time
import os
from azure.core.exceptions import HttpResponseError

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the Azure OpenAI Chat Completion client.
az_model_client = AzureOpenAIChatCompletionClient(
    azure_deployment=os.environ.get("AZURE_OPENAI_DEPLOYMENT"),
    model=os.environ.get("AZURE_OPENAI_DEPLOYMENT"),
    api_version=os.environ.get("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.environ.get("AZURE_OPENAI_API_ENDPOINT"),
    api_key=os.environ.get("AZURE_OPENAI_KEY"),
)

# Set your connection string (replace with your actual connection string)
project_connection_string = os.getenv("AZURE_AI_FOUNDRY_CONNECTION_STRING")

# Create the project client
project_client = AIProjectClient.from_connection_string(
    conn_str=project_connection_string, credential=DefaultAzureCredential()
)

async def branding_agent(query: str) -> str:
    """
    Create a marketing ad copy based on image description.

    Args:
        query (str): The image description.

    Returns:
        str: The text content retrieved from the first message of the agent's response.
    """

    print("Starting Bing search for Azure AI Agent Service...")

    with project_client:
        # Get the Bing search agent
        branding_ai_agent = project_client.agents.get_agent(agent_id="asst_F8CbpPd1CoL5gorrjZig1kRg")

        # Create a communication thread and send the user's query.
        thread = project_client.agents.create_thread()
        print(f"Created thread with ID: {thread.id}")

        project_client.agents.create_message(
            thread_id=thread.id,
            role="user",
            content=query,
        )
        print("User message sent.")

        # Run the agent process.
        run = project_client.agents.create_and_process_run(
            thread_id=thread.id, agent_id=branding_ai_agent.id
        )
        print(f"Run finished with status: {run.status}")

        # Create and process the run (combines creation + processing)
        try:
            tool_run = project_client.agents.create_and_process_run(
                thread_id=thread.id, agent_id=branding_ai_agent.id
            )
            print(f"Run created with initial status: {tool_run.status}")
        except HttpResponseError as e:
            print(f"Failed to create and process run: {e}")
            return

        # Polling to check the run status until completion
        try:
            while tool_run.status in ["queued", "in_progress", "requires_action"]:
                print(f"Current run status: {tool_run.status}")
                time.sleep(2)  # Wait for 2 seconds before checking again
                tool_run = project_client.agents.get_run(
                    thread_id=thread.id, run_id=tool_run.id
                )
                print(f"Updated run status: {tool_run.status}")
        except Exception as e:
            print("Error while polling run status.")
            return

        if run.status == "failed":
            print(f"Run failed with error: {run.last_error}")
            raise RuntimeError(f"Agent run failed: {run.last_error}")

        # Retrieve the result message BEFORE deleting the agent.
        messages = project_client.agents.list_messages(thread_id=thread.id)
        try:
            result_text = messages["data"][0]["content"][0]["text"]["value"]
        except (KeyError, IndexError) as e:
            raise RuntimeError("Failed to parse the result message.") from e

        print(f"Retrieved message: {result_text}")

    return result_text

# Define the Bing search agent using the web_ai_agent tool.
branding_agent = AssistantAgent(
    name="assistant",
    model_client=az_model_client,
    tools=[branding_agent],
    system_message="Use tools to solve tasks.",
)

async def assistant_run() -> None:
    """
    Runs the assistant agent to answer a query using the Bing search tool.
    """
    response = await branding_agent.on_messages(
        [
            TextMessage(
                content="A 4x6 inch Pattachira of Krishna and Radha, with a blue background and gold accents.",
                source="user",
            )
        ],
        cancellation_token=CancellationToken(),
    )
    print(response.chat_message)
    return response


import asyncio

if __name__ == "__main__":
    response = asyncio.run(assistant_run())