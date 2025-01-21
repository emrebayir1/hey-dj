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

tag_generation_prompt = PromptTemplate.from_template(
    """
    "The given text is intended to find relevant music tags for categorizing content. Please extract the tag from the text that is most relevant for music tagging.
    
    Your output must be a valid JSON object in the following format: 
    {{"search_query":"<output>"}}
    
    Please return only the output and no additional explanation.
    
    Example user input: 
    "Songs about love and heartbreak"
    
    Expected output: 
    {{"search_query":"love"}}
    
    User input: {input}
    
    Expected output:
    """
)

tag_generation_chain = tag_generation_prompt | llm | pydantic_parser

def tag_generator(state:GraphState) -> Dict[str, Any]:
    """
    Generates tag based on user's request.
    Attributes:
        state (dict): Current state of the graph.
    Returns:
        state (dict): LLM generated tag.
    """
    input = state["input"]
    search_query = tag_generation_chain.invoke({"input":input})
    return {"input":input, "search_query":search_query}