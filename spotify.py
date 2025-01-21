import os
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import lyricsgenius as lg

# Secrets Management
load_dotenv()
SP_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SP_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SP_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")
LG_ACCESS_TOKEN = os.getenv("GENIUS_ACCESS_TOKEN")
LFM_API_KEY = os.getenv("LASTFM_API_KEY") # LastFm is used for tag related search operations.
LFM_URL = "http://ws.audioscrobbler.com/2.0/"
SCOPE = "user-read-private, playlist-modify-private, playlist-modify-public" # Necessary scopes for Spotify API.

# Spotify object for Spotify related operations.
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SP_CLIENT_ID,
                                               client_secret=SP_CLIENT_SECRET,
                                               redirect_uri=SP_REDIRECT_URI,
                                               scope=SCOPE))


# genius object for lyric search functionality.
genius = lg.Genius(LG_ACCESS_TOKEN, skip_non_songs=True, excluded_terms=["(Remix)", "(Live)", "-", "Remaster"], remove_section_headers=True)

def search_songs(query="", limit=25):
    """
    Searches for tracks on Spotify.

    Args:


    Returns:
        list: A list of URIs for the matching tracks.
    """

    results = sp.search(q=query, type="track", limit=limit)

    track_uris = []
    if 'tracks' in results and 'items' in results['tracks']:
        for track in results['tracks']['items']:
            if 'uri' in track:
                track_uris.append(track['uri'])

    return track_uris

def search_songs_by_name(artist="", track="", limit=25):
    """
    Searches for tracks on Spotify based on artist, track name.

    Args:
        artist (str): Name of the artist (default: "").
        track (str): Name of the track (default: "").
        limit (int): Maximum number of results to return (default: 25).

    Returns:
        list: A list of URIs for the matching tracks.
    """
    query = []
    if artist:
        query.append(f"artist:{artist}")
    if track:
        query.append(f"track:{track}")

    query_string = ", ".join(query)

    results = sp.search(q=query_string, type="track", limit=limit)

    track_uris = []
    if 'tracks' in results and 'items' in results['tracks']:
        for track in results['tracks']['items']:
            if 'uri' in track:
                track_uris.append(track['uri'])

    return track_uris


def search_songs_by_lyrics(query="", limit=25):
    """
    Searches for songs based on lyrics and retrieves their URIs.

    Attributes:
        query (str): The lyrics or part of the lyrics to search for.
        limit (int): The maximum number of song URIs to return.

    Returns:
        track_uris (list): A list of track URIs corresponding to the found songs.
    """
    def get_song_info(data):
        """Extracts song details (artist and track name) from the search result data."""
        songs = []
        for hit in data.get("hits", []):
            result = hit.get("result", {})
            artist = result.get("artist_names")
            track = result.get("title")
            if artist and track:  #
                songs.append({"artist": artist, "track": track})
        return songs


    # Genius API only allows 20 result per page. This part fetch song details across multiple pages if necessary.
    def fetch_song_info_by_page(lyrics, per_page, page):
        """Fetches song information from a specific page of the search results."""
        search_result = genius.search(lyrics, per_page=per_page, page=page)
        return get_song_info(search_result)

    tracks = []
    track_uris = []
    remaining_limit = limit
    page = 1

    while remaining_limit > 0:
        per_page = min(remaining_limit, 20)
        tracks.extend(fetch_song_info_by_page(query, per_page, page))
        remaining_limit -= per_page
        page += 1

    for track in tracks:
        artist = track['artist']
        track_name = track['track']
        track_uri = search_songs_by_name(artist=artist, track=track_name, limit=1)

        if not track_uri:
            track_uri = search_songs(query=query, limit=1)

        track_uris.extend(track_uri)

    return track_uris

def search_songs_by_tag(query="", limit=25):
    """
    Searches for songs by a specific tag and retrieves their URIs.

    Attributes:
        query (str): The tag to search for (e.g., genre, mood).
        limit (int): The maximum number of song URIs to return.

    Returns:
        track_uris (list): A list of track URIs corresponding to the found songs.
    """
    url = f"{LFM_URL}?method=tag.gettoptracks&tag={query}&api_key={LFM_API_KEY}&format=json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        tracks = data['tracks']['track']
        track_list = []
        track_uris = []

        for track in tracks[:limit]:
            track_info = {"artist": track['artist']['name'], "track": track['name']}
            track_list.append(track_info)

        for song in track_list:
            track = song['track']
            artist = song['artist']
            track_uri = search_songs_by_name(artist=artist, track=track, limit=1)
            if not track_uri:
                track_uri = search_songs(query=query, limit=1)
            track_uris.extend(track_uri)
        return track_uris

    else:
        print("Error occured:", response.status_code)
        return []


def create_playlist(name="", description="", tracks=[]):
    """
    Creates a new playlist on Spotify and adds specified tracks to it.

    Attributes:
        name (str): The name of the playlist.
        description (str): The description of the playlist.
        tracks (list): A list of track URIs to be added to the playlist.

    Returns:
        playlist_url (str): The URL of the created playlist on Spotify.
    """
    user = sp.current_user()
    user_id = user['id']
    generated_playlist = sp.user_playlist_create(user=user_id, name=name, description=description)
    generated_playlist_id = generated_playlist['id']
    sp.playlist_add_items(playlist_id=generated_playlist_id, items=tracks)
    playlist_url = generated_playlist['external_urls']['spotify']
    return playlist_url

def get_spotify_oauth():
    """
    Returns an instance of SpotifyOAuth to handle the authentication process.

    Attributes:
        None

    Returns:
        SpotifyOAuth: An instance configured with the necessary credentials and scope.
    """
    return SpotifyOAuth(
        client_id=SP_CLIENT_ID,
        client_secret=SP_CLIENT_SECRET,
        redirect_uri=SP_REDIRECT_URI,
        scope=SCOPE
    )