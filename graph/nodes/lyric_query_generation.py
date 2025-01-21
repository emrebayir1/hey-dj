from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from graph.models import text_generator_llm
from graph.state import GraphState
from typing import Dict, Any
llm = text_generator_llm

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

lyric_query_generation_prompt = PromptTemplate.from_template(
    """
    "The given text is intended to find keywords for searching song lyrics. Please extract the keyword from the text that is most relevant for song lyrics search. The output should only be this keyword.
    
    Your output must be a valid JSON object in the following format:  
    {{"search_query":"<output>"}}
    
    Example user input:
    "Songs with the word love in the lyrics"
    
    Expected output:
    {{"search_query":"love"}}
    
    User input: 
    {input}
    
    Expected output:
    """
)

lyric_query_generation_chain = lyric_query_generation_prompt | llm | pydantic_parser

def lyric_query_generator(state:GraphState) -> Dict[str, Any]:
    """
    Generates lyric query based on user's input to use in search operations.
    Attributes:
        state (dict): Current state of the graph.
    Returns:
        state (dict): LLM generated lyric query.
    """
    input = state['input']
    search_query = lyric_query_generation_chain.invoke({"input":input})
    return {"input":input, "search_query":search_query}

