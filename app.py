from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_agentchat.teams import SelectorGroupChat
import os
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from autogen_agentchat.ui import Console
from src.tools.azure_agent_wrapper import branding_agent, cataloger_agent, onboarding_agent,visual_insight_agent,seo_agent,user_proxy,planning_agent,selector_prompt
from src.tools.agent_tools import image_describing_tool
from utils.llm_config import config_list

az_model_client = AzureOpenAIChatCompletionClient(
    azure_deployment="gpt-4o",
    model="gpt-4o",
    api_version=os.environ.get("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.environ.get("AZURE_OPENAI_API_ENDPOINT"),
    api_key=os.environ.get("AZURE_OPENAI_KEY"),
)

llm_config = {"config_list": config_list, "seed": 52}

file = r'images\image2.jpg'
image_description = image_describing_tool(file)
task_prompt = (
    "I need to have the marketing copy for a product, please follow these steps to create the copy:\n\n"
    "1. Visually Analyze the image description: {}'\n"
    "2. Create marketing and other related product description'\n"
    "3. Make sure the descriptions and other information is SEO friendly'\n"
    "4. Save the product in catalog'\n\n"
    "Using the gathered information, collaboratively write a compelling marketing ad copy"
    "Once the content is finalized, save it.".format(image_description)
)

text_mention_termination = TextMentionTermination("TERMINATE")
max_messages_termination = MaxMessageTermination(max_messages=50)
termination = text_mention_termination | max_messages_termination

team = SelectorGroupChat(
    [planning_agent, 
    branding_agent, 
    cataloger_agent,
    visual_insight_agent,
    seo_agent,
    user_proxy],
    model_client=az_model_client,
    termination_condition=termination,
    selector_prompt=selector_prompt,
    allow_repeated_speaker=True,  # Allow an agent to speak multiple turns in a row.
)

task = task_prompt

import asyncio

async def main():
    await Console(team.run_stream(task=task))

asyncio.run(main())