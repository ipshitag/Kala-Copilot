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
    with open(r"C:\Users\souga\Downloads\_Github_local\Retail-Copilot-Hackathon\src\tools\prompts\final-output-system-prompt.txt", "r") as file:
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
    with open("conversation_history.txt", "r") as file:
        ch = file.read()
    user_profile_json = get_final_user_profile(ch)
    print(user_profile_json)