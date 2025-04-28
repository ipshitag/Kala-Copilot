## import dependencies
from langchain import hub
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_openai import AzureChatOpenAI
from langchain_community.tools.bing_search import BingSearchResults
from langchain_community.utilities import BingSearchAPIWrapper
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from typing import Dict
import json

## environment setup
import os
from dotenv import load_dotenv
load_dotenv()
os.environ["AZURE_OPENAI_API_KEY"] = os.getenv("AZURE_OPENAI_KEY")
os.environ["AZURE_OPENAI_ENDPOINT"] = os.getenv("AZURE_OPENAI_ENDPOINT")
os.environ["AZURE_OPENAI_API_VERSION"] = os.getenv("AZURE_OPENAI_API_VERSION")
os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"] = os.getenv("AZURE_OPENAI_DEPLOYMENT")

def reformat_input(art_description: str) -> str:
    """
    Reformat the input art description JSON to include only productName and productDescription fields.

    Args:
        art_description (str): JSON string containing art description.

    Returns:
        str: Reformatted JSON string with selected fields.
    """
    art_description = json.loads(art_description)
    return json.dumps({key: art_description[key] for key in ["productName", "productDescription"]})

def generate_search_query(art_description: str) -> str:
    """
    Generate a search query string from the given art description using Azure OpenAI and a prompt template.

    Args:
        art_description (str): JSON string containing art description.

    Returns:
        str: Generated search query string.
    """
    art_description = reformat_input(art_description)
    ## object for structured output
    class BingSearchQuery(BaseModel):
        search_query: str = Field(description="LLM generated search query based on the art description provided")

    with open("prompts/search-query-formation-prompt.txt", "r") as file:
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

def bing_search(search_query: str) -> Dict:
    """
    Perform a Bing search using a given search query with the help of an LLM agent and the Bing API.

    Args:
        search_query (str): The search query string to search for.

    Returns:
        dict: Search results obtained from Bing.
    """
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
    return results

def get_art_price_range(search_results: Dict) -> Dict:
    """
    Estimate the minimum and maximum price range of an artwork based on Bing search results.

    Args:
        search_results (dict): Search results obtained from Bing.

    Returns:
        dict: Estimated price range and reasoning in INR (Indian Rupees).
    """
    class Artprice(BaseModel):
        reasoning: str = Field(description="Brief explanation of how the price range was determined based on the search results.")
        minimum_price: float = Field(description="Estimated minimum price of the artwork in Indian Rupees (INR).")
        maximum_price: float = Field(description="Estimated maximum price of the artwork in Indian Rupees (INR).")
    parser = JsonOutputParser(pydantic_object=Artprice)
    with open(r"prompts/final-bing-search-prompt.txt", "r") as file:
        system_prompt_template = file.read()
    llm = AzureChatOpenAI(
        openai_api_key=os.environ["AZURE_OPENAI_API_KEY"],
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
        openai_api_version=os.environ["AZURE_OPENAI_API_VERSION"],
    )
    prompt = PromptTemplate(
        template=system_prompt_template,
        input_variables=["search_results"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    chain = prompt | llm | parser
    results = chain.invoke({"search_results": json.dumps(search_results)})
    dollar_exchange_rate = 85
    results['minimum_price'] = round(results.get("minimum_price", 0)/dollar_exchange_rate, 0)
    results['maximum_price'] = round(results.get("maximum_price", 0)/dollar_exchange_rate, 0)
    return results

if __name__=="__main__":
    """
    Main execution block: Reads art description from file, generates search query,
    performs Bing search, and estimates artwork price range.
    """
    with open(r"example_delete_later\search-input.json", "r") as file:
        image_description = file.read()
    search_query = generate_search_query(art_description=image_description)
    search_result = bing_search(search_query=search_query)
    final_results = get_art_price_range(search_results=search_result)
    print("\n\n\n")
    print(f">> Search Query: {search_query}")
    print(f">> Final Output: {search_result}")
    print("\n\n\n")
    print(f"Final Output: {final_results}")