import spotipy
from graph.compiler import playlist_info_generator
from spotify import search_songs, search_songs_by_lyrics, search_songs_by_tag, create_playlist, sp, get_spotify_oauth
import pandas as pd
import streamlit as st

def get_search_results(playlist_info, limit):
    """
    Retrieves search results for songs based on the LLM generated search method and query.

    Attributes:
        playlist_info (dict): Contains the search parameters, including:
            - search_query (str): The query string for the search.
            - search_function (str): Specifies the type of search. Possible values:
                - 'search_songs': Search by song titles.
                - 'search_songs_by_lyrics': Search by lyrics.
                - 'search_songs_by_tag': Search by tags.
        limit (int): The maximum number of search results to return.

    Returns:
        search_results (list): The track URI'S obtained from the specified search method.
    """
    search_query = playlist_info['search_query']
    search_function = playlist_info['search_function']
    if search_function == 'search_songs':
        search_results = search_songs(query=search_query, limit=limit)
    elif search_function == 'search_songs_by_lyrics':
        search_results = search_songs_by_lyrics(query=search_query, limit=limit)
    elif search_function == 'search_songs_by_tag':
        search_results = search_songs_by_tag(query=search_query, limit=limit)
    return search_results


def generate_playlist_dataframe(search_results):
    """
    Creates a pandas DataFrame containing playlist details from track URI's.

    Attributes:
        search_results (list): A list of track URIs retrieved from a search.
    Returns:
        df (pd.DataFrame): A DataFrame with the following columns:
            - Track No: The track's position in the playlist (starting from 1).
            - Album Image: HTML code displaying the album's cover image.
            - Track Name: The name of the track.
            - Artist Name: The name(s) of the artist(s), separated by commas.
    """
    track_data = []
    for uri in search_results:
        track = sp.track(uri)  # Fetches track details from Spotify's API.
        track_name = track['name']
        artist_name = ', '.join(artist['name'] for artist in track['artists'])
        album_image = track['album']['images'][0]['url'] if track['album']['images'] else None
        album_image_html = f'<img src="{album_image}" width="60">' if album_image else "No Image"

        track_data.append({
            "Album Image": album_image_html,
            "Track Name": track_name,
            "Artist Name": artist_name,
        })

    df = pd.DataFrame(track_data)
    df.insert(0, "Track No", range(1, len(df) + 1))
    return df

## STREAMLIT

st.set_page_config(
    page_title="Hey DJ - AI Powered Spotify Playlist Creator",
    page_icon="🎹",
)
st.title("🎹 HeyDJ - Your AI Powered Spotify Playlist Creator")
st.text("""
HeyDJ is an AI-powered music companion that creates personalized playlists based on your input. Whether you're searching for songs by lyrics, genre, or title, HeyDJ helps you find the perfect tunes in seconds.

Simply type a few words, and HeyDJ crafts the playlist, synced with Spotify. 🎶
""")
st.text("""

""")

# Slider for song number in a playlist.
limit = st.select_slider("**Number of Tracks**:", options=list(range(1, 31)), value=15)

# User query.
user_input = st.text_area("**Your Playlist Idea**:", placeholder="Songs for a road trip with friends.")

# Creating states for Streamlit App to manage playlist generation and user token data
# These states will track whether a playlist has been generated, store relevant playlist information,
# maintain search results, and handle user token information.
if 'playlist_generated' not in st.session_state:
    st.session_state.playlist_generated = False
    st.session_state.playlist_info = None
    st.session_state.search_results = None
    st.session_state.playlist_df = None
if 'token_info' not in st.session_state:
    st.session_state.token_info = None

# When the "Generate Playlist" button is clicked, the following block of code is executed
if st.button(label="▷ Generate Playlist", use_container_width=True):
    # Initialize a progress bar and a status text area
    progress_bar = st.progress(0)
    status_text = st.empty() # Placeholder

    # Step 1: Generate playlist title and description
    status_text.text("Generating playlist title and description...")
    playlist_info = playlist_info_generator(user_input) # LLM generated playlist info dictionary.
    st.session_state.playlist_generated = True # Update the streamlit state
    st.session_state.playlist_info = playlist_info
    progress_bar.progress(50) # Update progress bar to indicate 50% completion

    # Step 2: Search for songs based on the generated playlist information
    status_text.text("Searching for songs...")
    search_results = get_search_results(playlist_info, limit)
    playlist_df = generate_playlist_dataframe(search_results)
    st.session_state.search_results = search_results # Update the streamlit state
    st.session_state.playlist_df = playlist_df # Update the streamlit state
    progress_bar.progress(100) # Update progress bar to indicate 100% completion

    # Step 3: Clear progress bar and display final status
    progress_bar.empty() # Remove the progress bar
    status_text.text("Here is the playlist:")

    # Display the generated playlist information
    st.subheader(f"Playlist Name: {playlist_info['playlist_name']}", divider=True)
    st.subheader("Description")
    st.write(playlist_info['description'], divider=True)
    st.write("### Tracks", divider=True)
    st.markdown(
        playlist_df.to_html(escape=False, index=False),  # Convert the DataFrame to an HTML table with embedded HTML enabled to show Album Images properly.
        unsafe_allow_html=True # Allow the HTML content to be rendered directly
    )

# Check if the playlist has been generated (session state flag)
if st.session_state.playlist_generated:
    # Create two columns for the 'Add to Spotify' and 'Cancel' buttons
    left, right = st.columns(2)

    # Left column: 'Add to Spotify' button functionality
    if left.button(label="Add to Spotify", use_container_width=True):
        if st.session_state.token_info:
            playlist_info = st.session_state.playlist_info
            search_results = st.session_state.search_results
            playlist = create_playlist(name=playlist_info['playlist_name'], description=playlist_info['description'],
                                       tracks=search_results)
            st.success('Playlist Generated!', icon="✅")
            st.link_button("Go to the Playlist", f"{playlist}", use_container_width=True)
        else:
            st.error("Please login to Spotify to access this feature.")

    # Right column: 'Cancel' button functionality
    if right.button(label="Cancel", use_container_width=True):
        # Reset session state variables to their initial state (no playlist)
        st.session_state.playlist_generated = False
        st.session_state.playlist_info = None
        st.session_state.search_results = None
        st.session_state.playlist_df = None
        st.empty() # Clear any remaining UI elements (like the progress bar or status text)

# Create a sidebar for account-related actions and information
with st.sidebar:
    st.header("Account Info")
    st.text("You must authenticate with Spotify to add the generated playlist to your account.")
    if st.button("Authenticate with Spotify", use_container_width=True):
        # Get the Spotify OAuth object and generate the authentication URL
        sp_oauth = get_spotify_oauth()
        auth_url = sp_oauth.get_authorize_url()
        st.write("**1.** Click the link below to authenticate with Spotify:")
        st.write(f"[Click here.]({auth_url})")
        st.write("**2.** After authenticating, paste the URL you were redirected to below:")

    # Input field to paste the redirect URL received after authenticating
    redirect_url = st.text_input("Redirect URL", placeholder="Paste the redirected URL here")

    # If the user has entered the redirect URL, attempt to authenticate
    if redirect_url:
        try:
            # Parse the code from the redirect URL and get the access token
            sp_oauth = get_spotify_oauth()
            code = sp_oauth.parse_response_code(redirect_url)
            token_info = sp_oauth.get_access_token(code)

            # Store the token information in the session state for later use
            st.session_state.token_info = token_info
            token=st.session_state.token_info["access_token"]
            sp = spotipy.Spotify(auth=token)

            # Get the current user's Spotify profile information and display.
            user_info = sp.current_user()
            st.success("Authentication successful!")
            st.subheader("Your Spotify Profile")
            st.write(f"**Name:** {user_info['display_name']}")
            st.write(f"**Spotify ID:** {user_info['id']}")
        except Exception as e:
            st.error(f"Authentication failed: {e}")