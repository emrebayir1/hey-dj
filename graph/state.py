from typing import TypedDict

# State object for LangGraph to handle the flow.
class GraphState(TypedDict):
    """
    Represents the state of a graph.
    Attributes:
        input: User's input.
        description: Generated playlist description.
        lyric_query: Lyric query to search.
        playlist_name: Generated playlist name.
        search_function: Chosen search function to use.
        search_query: Search query to search.
        music_tag: Music tag to search.
    """
    input: str
    description: str
    lyric_query: str
    playlist_name: str
    search_function: str
    search_query: str
    music_tag: str