from graph.nodes.description_generation import description_generator
from graph.nodes.lyric_query_generation import lyric_query_generator
from graph.nodes.playlist_name_generation import playlist_name_generator
from graph.nodes.query_classification import query_classifier
from graph.nodes.search_query_generation import search_query_generator
from graph.nodes.tag_generation import tag_generator
from graph.state import GraphState
from langgraph.graph import StateGraph, START, END

# LangGraph Workflow
workflow = StateGraph(GraphState)

# Conditional Edges
def search_query_router(state:GraphState):
    search_function = state.get("search_function")
    if search_function == "search_songs":
        return "search_songs"
    elif search_function == "search_songs_by_lyrics":
        return "search_songs_by_lyrics"
    else:
        return "search_songs_by_tag"


# Nodes
workflow.add_node("description_generator", description_generator)
workflow.add_node("lyric_query_generator", lyric_query_generator)
workflow.add_node("playlist_name_generator", playlist_name_generator)
workflow.add_node("query_classifier", query_classifier)
workflow.add_node("search_query_generator", search_query_generator)
workflow.add_node("tag_generator", tag_generator)

# Workflow
workflow.add_edge(START, "query_classifier")
workflow.add_conditional_edges("query_classifier", search_query_router,
                               {
                                   "search_songs":"search_query_generator",
                                   "search_songs_by_lyrics":"lyric_query_generator",
                                   "search_songs_by_tag":"tag_generator",
                               }
                               )
workflow.add_edge("search_query_generator","playlist_name_generator")
workflow.add_edge("lyric_query_generator","playlist_name_generator")
workflow.add_edge("tag_generator","playlist_name_generator")
workflow.add_edge("playlist_name_generator","description_generator")
workflow.add_edge("description_generator",END)
compiled_workflow = workflow.compile()

# Main Function.
def playlist_info_generator(input=""):
    """
    Generates playlist-related information based on user input.

    This function processes the input through a workflow to:
    1. Determine the appropriate search function (songs, lyrics, or tags).
    2. Generate a search query and playlist name.
    3. Create a description for the playlist.

    Attributes:
        input (str): User input (e.g., a search query).

    Returns:
        dict: A dictionary containing:
            - "input": The original user input.
            - "description": Generated playlist description.
            - "playlist_name": Suggested playlist name.
            - "search_function": The determined search function.
            - "search_query": Generated search query.
    """
    input_dict = {"input": input}
    result = compiled_workflow.invoke(input_dict)
    playlist_info = {
        "input": result["input"],
        "description": result["description"].description,
        "playlist_name": result["playlist_name"].playlist_name,
        "search_function": result["search_function"].search_function,
        "search_query": result["search_query"].search_query
    }
    return playlist_info