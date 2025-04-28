import os
import asyncio
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from src.tools.azure_agent_wrapper import branding_agent, cataloger_agent, onboarding_agent,visual_insight_agent,seo_agent,user_proxy,planning_agent,selector_prompt
from src.tools.agent_tools import image_describing_tool
from utils.llm_config import config_list
import asyncio

az_model_client = AzureOpenAIChatCompletionClient(
    azure_deployment="gpt-4o",
    model="gpt-4o",
    api_version=os.environ.get("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.environ.get("AZURE_OPENAI_API_ENDPOINT"),
    api_key=os.environ.get("AZURE_OPENAI_KEY"),
)

llm_config = {"config_list": config_list, "seed": 52}

# Step 1: Get image description  
file = r'images\image1.jpg'
image_description = image_describing_tool(file)

async def run_agent(agent, task_template, message_source, input_text):
    task = task_template.format(input_text)
    result = await agent.run(task=task)
    for message in result.messages:
        if getattr(message, "source", None) == message_source:
            return message.content

# Step 2: Run visual_insight_agent
visual_task_template = "Create a polished and stunning description of, treat the image as a product: {}"
visual_agent_result = asyncio.run(
    run_agent(
        agent=visual_insight_agent,
        task_template=visual_task_template,
        message_source="visual_insight_agent",
        input_text=image_description
    )
)

# Step 3: Run branding_agent
marketing_task_template = "Based on the following product description, create a marketing ad copy of the product: {}"
branding_agent_result = asyncio.run(
    run_agent(
        agent=branding_agent,
        task_template=marketing_task_template,
        message_source="branding_agent",
        input_text=visual_agent_result
    )
)

#step 4: Run seo_agent
seo_agent_task_template = "Create a SEO optimized product description for the following marketing copy: {}"
seo_agent_result = asyncio.run(
    run_agent(
        agent=seo_agent,
        task_template=seo_agent_task_template,
        message_source="seo_agent",
        input_text=branding_agent_result
    )
)

# Step 5: Run cataloger_agent
cataloger_agent_task_template = "Create a product catalog entry for the following marketing copy: {}"
cataloger_agent_result = asyncio.run(
    run_agent(
        agent=cataloger_agent,
        task_template=cataloger_agent_task_template,
        message_source="cataloger_agent",
        input_text=seo_agent_result
    )
)