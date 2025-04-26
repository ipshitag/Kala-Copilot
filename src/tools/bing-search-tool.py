## import dependencies
from langchain import hub
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_openai import AzureChatOpenAI
from langchain_community.tools.bing_search import BingSearchResults
from langchain_community.utilities import BingSearchAPIWrapper
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
import json

## environment setup
import os
from dotenv import load_dotenv
load_dotenv()
os.environ["AZURE_OPENAI_API_KEY"] = os.getenv("AZURE_OPENAI_KEY")
os.environ["AZURE_OPENAI_ENDPOINT"] = os.getenv("AZURE_OPENAI_ENDPOINT")
os.environ["AZURE_OPENAI_API_VERSION"] = os.getenv("AZURE_OPENAI_API_VERSION")
os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"] = os.getenv("AZURE_OPENAI_DEPLOYMENT")

def reformat_input(art_description: str):
    art_description = json.loads(art_description)
    return json.dumps({key: art_description[key] for key in ["productName", "productDescription"]})

def generate_search_query(art_description: str):
    art_description = reformat_input(art_description)
    ## object for structured output
    class BingSearchQuery(BaseModel):
        search_query: str = Field(description="LLM generated search query based on the art description provided")

    with open(r"C:\Users\souga\Downloads\_Github-local\Retail-Copilot-Hackathon\src\tools\prompts\search-query-formation-prompt.txt", "r") as file:
        query_formation_prompt_template = file.read()

    query_parser = JsonOutputParser(pydantic_object=BingSearchQuery)
    query_formation_prompt = PromptTemplate(
        template=query_formation_prompt_template,
        input_variables=["art_description"],
        partial_variables={"format_instructions": query_parser.get_format_instructions()}
    )
    
    llm = AzureChatOpenAI(
        openai_api_key=os.environ["AZURE_OPENAI_API_KEY"],
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
        openai_api_version=os.environ["AZURE_OPENAI_API_VERSION"]
    )

    chain = query_formation_prompt | llm | query_parser
    result = chain.invoke({"art_description": art_description})
    return result['search_query']

def bing_search(search_query: str):
    instructions = """You are an assistant."""
    base_prompt = hub.pull("langchain-ai/openai-functions-template")
    prompt = base_prompt.partial(instructions=instructions)
    llm = AzureChatOpenAI(
        openai_api_key=os.environ["AZURE_OPENAI_API_KEY"],
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
        openai_api_version=os.environ["AZURE_OPENAI_API_VERSION"],
    )
    bing_api_wrapper = BingSearchAPIWrapper(
        bing_subscription_key=os.getenv("AZURE_BING_KEY"),
        bing_search_url=os.getenv("https://api.bing.microsoft.com/v7.0/search"),
        search_kwargs={},
        k=10
    )
    tool = BingSearchResults(api_wrapper=bing_api_wrapper)
    tools = [tool]
    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
    )
    results = agent_executor.invoke({"input": search_query})
    return results['output']

if __name__=="__main__":
    with open("search-input.json", "r") as file:
        image_description = file.read()
    search_query = generate_search_query(art_description=image_description)
    search_result = bing_search(
        search_query=search_query
    )
    print("\n\n\n")
    print(f">> Search Query: {search_query}")
    print(f">> Final Output: {search_result}")