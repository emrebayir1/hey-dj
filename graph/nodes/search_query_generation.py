from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from graph.models import decidier_llm
from graph.state import GraphState
from typing import Dict, Any

llm = decidier_llm

class QueryGenerator(BaseModel):
    """
    Search query generator for using in search operations by transforming user's input into search query.
    """
    search_query: str =  Field(
        description="""
        A generated search query based on the user's input that will be used in search operations.
        """
    )

pydantic_parser = PydanticOutputParser(pydantic_object=QueryGenerator)

search_query_generation_prompt = PromptTemplate.from_template(
    """
    "Given the following natural language input, convert it into a query string that can be used in the search_song function on Spotify to find a song.
    
    The song title, artist, or any relevant detail can be included in the query, but focus on extracting the most relevant keywords and make sure the query is in the format suitable for a Spotify search.
    
    Your output must be valid JSON in the following dictionary format:
    {{"search_query": "<llm_result>"}}
        
    Input: '{input}'"
    
    Please return only the output and no additional explanation.
    """
)


search_query_generation_chain = search_query_generation_prompt | llm | pydantic_parser

def search_query_generator(state:GraphState) -> Dict[str, Any]:
    """
    Generates search query based on user's input.
    Attributes:
        state (dict): Current state of the graph.
    Returns:
        state (dict): LLM generated search query.
    """
    input = state["input"]
    search_query = search_query_generation_chain.invoke({"input":input})
    return {"input":input, "search_query":search_query}