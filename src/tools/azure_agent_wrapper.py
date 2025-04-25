from autogen_agentchat.agents import AssistantAgent,UserProxyAgent
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from pathlib import Path
import time
from src.tools.agent_tools import add_product_to_cosmos,add_users_to_cosmos
import os
from azure.core.exceptions import HttpResponseError


from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the Azure OpenAI Chat Completion client.
az_model_client = AzureOpenAIChatCompletionClient(
    azure_deployment="gpt-4o",
    model="gpt-4o",
    api_version=os.environ.get("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.environ.get("AZURE_OPENAI_API_ENDPOINT"),
    api_key=os.environ.get("AZURE_OPENAI_KEY"),
)

azure_deployment = "gpt-4o"
api_version = os.environ.get("AZURE_OPENAI_API_VERSION")
azure_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
api_key = os.environ.get("AZURE_OPENAI_KEY")

branding_agent_id = os.environ.get("BrandingAgent")
visualizer_agent_id = os.environ.get("VisualInsightAgent")
seo_agent_id = os.environ.get("SEOAgent")

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
        branding_ai_agent = project_client.agents.get_agent(agent_id=branding_agent_id)

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
                time.sleep(0.5)  # Wait for 2 seconds before checking again
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
    Create image description.

    Args:
        query (str): The image path.

    Returns:
        str: The text content retrieved from the first message of the agent's response.
    """

    print("Starting Image Description for Azure AI Agent Service...")

    with project_client:
        # Get the Bing search agent
        visualizor_ai_agent = project_client.agents.get_agent(agent_id=visualizer_agent_id)

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
                time.sleep(0.5)  # Wait for 2 seconds before checking again
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

async def SEO_agent(query: str) -> str:
    """
    Check for SEO Friendliness.

    Args:
        query (str): The image path.

    Returns:
        str: The text content retrieved from the first message of the agent's response.
    """

    print("Starting SEO Agent for Azure AI Agent Service...")

    with project_client:
        # Get the Bing search agent
        seo_agent = project_client.agents.get_agent(agent_id=seo_agent_id)

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
            thread_id=thread.id, agent_id=seo_agent.id
        )
        print(f"Run finished with status: {run.status}")

        # Create and process the run (combines creation + processing)
        try:
            tool_run = project_client.agents.create_and_process_run(
                thread_id=thread.id, 
                agent_id=seo_agent.id,
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
    name="branding_agent",
    description="An agent for creating marketing ad copy.",
    model_client=az_model_client,
    tools=[branding_agent],
    system_message="Use tools to solve tasks.",
)

visual_insight_agent = AssistantAgent(
    name="visual_insight_agent",
    description="An agent for describing images.",
    model_client=az_model_client,
    tools=[image_descriptor_agent],
    system_message="Use tools to solve tasks.",
)

cataloger_agent = AssistantAgent(
    name="cataloger_agent",
    description="An agent for saving product in catalog.",
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

seo_agent = AssistantAgent(
    name="seo_agent",
    description="An agent for checking SEO friendliness.",
    model_client=az_model_client,
    tools=[SEO_agent],
    system_message="Use tools to solve tasks.",
)

user_proxy = UserProxyAgent(
    name="Admin",
    description="A human admin. Interact with the planner to discuss the plan. Plan execution needs to be approved by this admin.",
)

planning_agent = AssistantAgent(
    "PlanningAgent",
    description="An agent for planning tasks, this agent should be the first to engage when given a new task.",
    model_client=az_model_client,
    system_message="""
    You are a planning agent.
    Your job is to break down complex tasks into smaller, manageable subtasks. Give time to the agents to complete their tasks. Verify data from user before cataloging.
    Your team members are:
        visual_insight_agent: Writes product descriptions based on image analysis
        branding_agent: Makes sure product descriptions are SEO friendly and creates marketing ad copy
        seo_agent: Checks for SEO friendliness of the content
        cataloger_agent: Saves the product in the catalog
        user_proxy: human admin who will approve the plan and execution

    You only plan and delegate tasks - you do not execute them yourself.

    When assigning tasks, use this format:
    1. <agent> : <task>

    After all tasks are complete, summarize the findings and end with "TERMINATE".
    """,
)

selector_prompt = """Select an agent to perform task.

{roles}

Current conversation context:
{history}

Read the above conversation, then select an agent from {participants} to perform the next task.
Make sure the planner agent has assigned tasks before other agents start working.
Only select one agent.
"""
