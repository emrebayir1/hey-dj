from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from graph.state import GraphState
from typing import Dict, Any
from graph.models import text_generator_llm

llm = text_generator_llm

class PlaylistNameGenerator(BaseModel):
    """
    Generator for playlist name by using user's input.
    """
    playlist_name: str = Field(
        description="""
        A genereated playlist name based on user's input.
        """
    )

pydantic_parser = PydanticOutputParser(pydantic_object=PlaylistNameGenerator)

playlist_name_prompt = PromptTemplate.from_template(
    """
    Given the user's prompt to create a playlist, generate a concise and meaningful playlist name. The playlist name should capture the essence of the user's input by focusing on the main artist, theme, or genre mentioned. Avoid unnecessary words like "generate", "create" or "playlist."  
    
    Your output must be a valid JSON object in the following format:  
    {{"playlist_name":"<output>"}}  
    
    Do not include any additional explanations or formatting.  
    
    Input: "{input}"  
    Output:  
    """
)

playlist_name_chain = playlist_name_prompt | llm | pydantic_parser

def playlist_name_generator(state:GraphState) -> Dict[str, Any]:
    """
    Generates playlist name based on user's input.
    Attributes:
        state (dict): Current state of the graph.
    Returns:
        state (dict): LLM generated playlist name.
    """
    input = state["input"]
    playlist_name = playlist_name_chain.invoke({"input":input})
    return {"input":input, "playlist_name":playlist_name}