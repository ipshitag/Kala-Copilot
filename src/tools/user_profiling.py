"""
User Profiling Script for Artist Onboarding

This script processes a conversation history to extract a structured user profile for an artist.
It uses a language model (Cohere via LangChain) and a prompt template to generate a JSON profile,
which includes details such as name, location, language preference, type of art, experience, and motivations.

Main Components:
- Environment setup and API key loading.
- Pydantic model for the artist's user profile.
- Function to generate the user profile from conversation history using a prompt and LLM.

Usage:
Run this script directly to read 'conversation_history.txt' and output a structured user profile in JSON format.
"""
## import dependencies
from langchain_cohere import ChatCohere
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from langchain.prompts import PromptTemplate
from json import dumps

## environment setup
import os
from dotenv import load_dotenv
load_dotenv()
os.environ['COHERE_API_KEY'] = os.getenv('COHERE_API_KEY')

class UserProfile(BaseModel):
    name_of_the_artist: str = Field(description="The full name of the artist as mentioned in the conversation")
    location: str = Field(description="Where the artist usually creates or showcases their art (e.g., city, street, area)", default="Unknown")
    language_preference: str = Field(description="The language the artist is most comfortable using for online content", default="Unknown")
    type_of_art: str = Field(description="A short description of the kind of art they create (e.g., murals, sketches, folk art)")
    years_of_experience: str = Field(description="How long the artist has been practicing their craft", default="Unknown")
    artist_story: str = Field(description="A brief background or origin story shared by the artist about their journey", default="Unknown")
    why_they_want_to_be_online: str = Field(description="The artist's motivation for building an online presence (e.g., reach more people, earn better)", default="Unknown")
    is_open_to_custom_orders: bool = Field(description="Whether the artist is willing to take on commissions or personalized art requests")

def get_final_user_profile(conversation_history: str):
    """
    Generate a structured user profile for the artist based on the provided conversation history.

    Args:
        conversation_history (str): The full text history of the onboarding conversation.

    Returns:
        str: The user profile as a JSON-formatted string.
    """
    with open(r"prompts/final-output-system-prompt.txt", "r") as file:
        system_prompt_template = file.read()
    parser = JsonOutputParser(pydantic_object=UserProfile)
    final_system_prompt = PromptTemplate(
        template=system_prompt_template,
        input_variables=["conversation_history"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    chatmodel = ChatCohere()
    chain = final_system_prompt | chatmodel | parser
    user_profile_info = chain.invoke({"conversation_history": conversation_history})
    return dumps(user_profile_info)    

if __name__=="__main__":
    with open("example_delete_later\conversation_history.txt", "r") as file:
        ch = file.read()
    user_profile_json = get_final_user_profile(ch)
    print(user_profile_json)