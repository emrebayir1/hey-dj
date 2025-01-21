from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from typing import Dict, Any
from graph.state import GraphState
from graph.models import decidier_llm

llm = decidier_llm

class QueryClassifier(BaseModel):
    """
    Classifier for deciding which search function to use.
    """
    search_function: str =  Field(
        description="""
        The chosen search function based on the user's query. 
        Possible values are: 'search_songs', 'search_songs_by_lyrics', or 'search_songs_by_tag'. This field represents the classifier's decision.
        """
    )

pydantic_parser = PydanticOutputParser(pydantic_object=QueryClassifier)

classification_prompt = PromptTemplate.from_template(
    """
    Your task is to analyze the given text and determine the user's intent based on their query. Choose and return only one of the following options in the form of a dictionary:
    
    1. {{"search_function": "search_songs"}} - If the user is looking for songs by name, artist, or making a general song search.
    2. {{"search_function": "search_songs_by_lyrics"}} - If the user is searching for a song based on its lyrics.
    3. {{"search_function": "search_songs_by_tag"}} - If the user is searching for songs based on tags like genre, mood, or theme.
    
    Input text: {input}
    
    Please return only one of the above options in dictionary format and no additional explanation.
    """

)

query_classification_chain = classification_prompt | llm | pydantic_parser

def query_classifier(state:GraphState) -> Dict[str, Any]:
    """
    Decides which search function to use.
    Attributes:
        state (dict): Current state of the graph.
    Returns:
        state (dict): LLM's decision.
    """
    input = state["input"]
    search_function = query_classification_chain.invoke({"input":input})
    return {"input":input, "search_function":search_function}
