from autogen_agentchat.agents import AssistantAgent,UserProxyAgent
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from pathlib import Path
import time
from .agent_tools import add_product_to_cosmos,add_users_to_cosmos
from .createAndPost import post_tweet_with_product
from .bing_search_tool import estimate_art_price_range
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
file_path_branding = r"src\tools\prompts\BrandingAgent.txt"
file_path_onboarding = r"src\tools\prompts\OnboardingAgent.txt"
file_path_visualizer = r"src\tools\prompts\VisualInsightsAgent.txt"
file_path_seo = r"src\tools\prompts\SEO_ExpertAgent.txt"
file_path_planning = r"src\tools\prompts\PlanningAgent.txt"
file_path_pricing = r"src\tools\prompts\PricingAgentPrompt.txt"
file_path_posting = r"src\tools\prompts\PostingAgentPrompt.txt"

# Set your connection string (replace with your actual connection string)
project_connection_string = os.getenv("AZURE_AI_FOUNDRY_CONNECTION_STRING")

# Create the project client
project_client = AIProjectClient.from_connection_string(
    conn_str=project_connection_string, credential=DefaultAzureCredential()
)


def read_file(file_path: str) -> str:
    """
    Read the content of a file.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: The content of the file.
    """
    file_path = Path(file_path)
    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        return file.read()

async def branding_marketing_agent(query: str) -> str:
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

branding_instructions = read_file(file_path_branding)
branding_agent = AssistantAgent(
    name="branding_agent",
    description="An agent that has specialized knowledge in creating marketing ad copy.",
    model_client=az_model_client,
    system_message=branding_instructions,
)

visualizer_instructions = read_file(file_path_visualizer)
visual_insight_agent = AssistantAgent(
    name="visual_insight_agent",
    description="An agent for creating accurate image descriptions from crude image descriptions.",
    model_client=az_model_client,
    system_message=visualizer_instructions,
)

cataloger_instructions = read_file(file_path_cataloger)
cataloger_agent = AssistantAgent(
    name="cataloger_agent",
    description="An agent for saving product in catalog database.",
    model_client=az_model_client,
    tools=[add_product_to_cosmos],
    system_message=cataloger_instructions,
)

onboarding_instructions = read_file(file_path_onboarding)
onboarding_agent = AssistantAgent(
    name="onboarding_agent",
    model_client=az_model_client,
    tools =[add_users_to_cosmos],
    system_message=onboarding_instructions,
)

seo_instructions = read_file(file_path_seo)
seo_agent = AssistantAgent(
    name="seo_agent",
    description="An agent for checking SEO friendliness in the market copy.",
    model_client=az_model_client,
    system_message=seo_instructions,
)

user_proxy = UserProxyAgent(
    name="Admin",
    description="The human user who will approve the tasks.",
)

planning_instructions = read_file(file_path_planning)
planning_agent = AssistantAgent(
    "PlanningAgent",
    description="An agent for planning tasks, this agent should be the first to engage to the user. This agent should not perform any tasks.",
    model_client=az_model_client,
    system_message=file_path_planning,
)

pricing_instructions = read_file(file_path_pricing)
pricing_agent = AssistantAgent(
    name="pricing_agent",
    description="An agent for checking the price range of the artwork.",
    model_client=az_model_client,
    tools=[estimate_art_price_range],
    system_message=pricing_instructions,
)

posting_instructions = read_file(file_path_posting)
posting_agent = AssistantAgent(
    name="posting_agent",
    description="An agent for posting the product on the website.",
    model_client=az_model_client,
    system_message=posting_instructions,
    tools=[post_tweet_with_product]
)

selector_prompt = """Select an agent to perform task.

{roles}

Current conversation context:
{history}

Read the above conversation, then select an agent from {participants} to perform the next task.
When the task is complete, let the user approve or disapprove the task.

Make sure to ask the user for language preference as they might not be english native.
Every task should be dont by its respective agent, planning agent should NOT perform any task.
All agents should be able to ask the user for any additional information and approvals.
Please make sure the agents are called in the order of their workflow.

Workflow:
    *  PlanningAgent: Ask user for language preference
    *  user_proxy: response from user
    0. PlanningAgent: Create a plan for the task and ask user for approval
    1. visual_insight_agent : Provides accurate description of image
    2. branding_agent : Creates branding stuff/narrative
    3. seo_agent : check SEO friendliness
    4. cataloger_agent : save to database
"""