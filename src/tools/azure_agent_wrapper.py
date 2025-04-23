from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from pathlib import Path
import time
from agent_tools import add_product_to_cosmos,add_users_to_cosmos
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

azure_deployment = os.environ.get("AZURE_OPENAI_DEPLOYMENT")
api_version = os.environ.get("AZURE_OPENAI_API_VERSION")
azure_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
api_key = os.environ.get("AZURE_OPENAI_KEY")

file_path_cataloger = r"src\tools\prompts\CatalogerAgent.txt"
file_path_cataloger = Path(file_path_cataloger)

with file_path_cataloger.open("r", encoding="utf-8", errors="ignore") as file:
            cataloger_instructions = file.read()


file_path_onboarding = r"src\tools\prompts\OnboardingAgent.txt"
file_path_onboarding = Path(file_path_onboarding)

with file_path_onboarding.open("r", encoding="utf-8", errors="ignore") as file:
            onboarding_instructions = file.read()

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

async def image_descriptor_agent(query: str) -> str:
    """
    Create image description based on file path.

    Args:
        query (str): The image path.

    Returns:
        str: The text content retrieved from the first message of the agent's response.
    """

    print("Starting Image Description for Azure AI Agent Service...")

    with project_client:
        # Get the Bing search agent
        visualizor_ai_agent = project_client.agents.get_agent(agent_id="asst_7yZ3gUgza6jWfSH4Z6Wj1AcT")

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
            thread_id=thread.id, agent_id=visualizor_ai_agent.id
        )
        print(f"Run finished with status: {run.status}")

        # Create and process the run (combines creation + processing)
        try:
            tool_run = project_client.agents.create_and_process_run(
                thread_id=thread.id, 
                agent_id=visualizor_ai_agent.id,
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

    return result_text

branding_agent = AssistantAgent(
    name="assistant",
    model_client=az_model_client,
    tools=[branding_agent],
    system_message="Use tools to solve tasks.",
)

visual_insight_agent = AssistantAgent(
    name="visual_insight_agent",
    model_client=az_model_client,
    tools=[image_descriptor_agent],
    system_message="Use tools to solve tasks.",
)

cataloger_agent = AssistantAgent(
    name="cataloger_agent",
    model_client=az_model_client,
    tools=[add_product_to_cosmos],
    system_message=cataloger_instructions,
)

onboarding_agent = AssistantAgent(
    name="onboarding_agent",
    model_client=az_model_client,
    tools=[add_users_to_cosmos],
    system_message=onboarding_instructions,
)