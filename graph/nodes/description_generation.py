from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from graph.models import text_generator_llm
from graph.state import GraphState
from typing import Any, Dict

llm = text_generator_llm

class DescriptionGenerator(BaseModel):
    """
    Generator for playlist description by using user's input and generated playlist name.
    """
    description: str = Field(
        description="""
        A generated playlist description based on user's input and generated playilst name
        """
    )

pydantic_parser = PydanticOutputParser(pydantic_object=DescriptionGenerator)

description_prompt = PromptTemplate.from_template(
    """
    Given the user's prompt to create a playlist and the generated playlist name, craft a compelling and engaging playlist description. The description should reflect the theme, mood, or essence of the playlist while being concise and appealing. Avoid repeating the playlist name directly but ensure the description aligns with it.  

    Your output must be a valid JSON object in the following format:  
    {{"description":"<output>"}} 
    
    The output should always be in the same language as the user's input. 
    
    Inputs:  
    Playlist Name: "{playlist_name}"  
    User's Prompt: "{input}"  
    
    Output:  
    """
)

description_chain = description_prompt | llm | pydantic_parser

def description_generator(state:GraphState) -> Dict[str, Any]:
    """
    Generates playlist description based on user's input and playlist name.
    Attributes:
        state (dict): Current state of the graph.
    Returns:
        state (dict): LLM generated playlist description.
    """
    input = state['input']
    playlist_name = state['playlist_name']
    description = description_chain.invoke({"input":input, "playlist_name":playlist_name})
    return {"input":input, "playlist_name":playlist_name, "description":description}