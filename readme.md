# HeyDJ - AI Powered Spotify Playlist Generator

## Introduction

HeyDJ is an AI-powered music companion that allows users to create personalized Spotify playlists based on their input. Whether you're searching for songs by lyrics, genre, or title, HeyDJ helps you find the perfect tracks in seconds. With the integration of Spotify's API, HeyDJ creates playlists tailored to your preferences.

## Demo

Here is a demo of the app on Streamlit Cloud platform:
### [HeyDJ](https://hey-dj.streamlit.app)

## Features

* **AI Powered Playlist Generation:** Input your playlist idea, and HeyDJ uses AI to generate a relevant playlist.
* **Multiple Search Methods:** Search for songs by title, lyrics, or tag to match your playlist's theme. HeyDJ decides which search method to use.
* **Spotify Integration:** Create and add playlists to your Spotify account.
* **Llama Model:** `llama-3.3-70b-versatile` is used to generate intelligent playlist titles, descriptions, and search queries based on the user’s input.
* **LangGraph Integration:**  HeyDJ utilizes LangGraph to enhance the AI's understanding of playlist context and generate more accurate playlist information.
* **Streamlit User Interface:** Built with Streamlit for easy interaction and a clean user interface.

## How To Use

* **1:** Select the number of tracks you want to include in your playlist.
* **2:** Enter a brief description of your playlist idea (e.g., "Songs for a road trip") and click "▷ Generate Playlist".
* **3:** HeyDJ will generate a title and description for your playlist search for songs that fit the generated playlist parameters based on your input. A list of songs is displayed with album art, track names, and artist names. If you're logged into your Spotify account, you can add the playlist directly to your Spotify library.

## Authentication

* **1:** Click on the "Authenticate with Spotify" button in the sidebar.
* **2:** Follow the link to authenticate your account.
* **3:** Paste the redirected URL back into the input field to authenticate.

## Required API's

To use this project, you need to obtain the following API keys. Please follow the respective documentation to register and get access tokens or keys.

### 1. [Spotify API](https://developer.spotify.com/documentation/web-api)
- **SPOTIPY_CLIENT_ID**: Your Spotify Client ID.
- **SPOTIPY_CLIENT_SECRET**: Your Spotify Client Secret.
- **SPOTIPY_REDIRECT_URI**: Set the redirect URI for authentication (default: `'https://localhost:8501/callback'`).

### 2. [Genius API](https://docs.genius.com/)
- **GENIUS_ACCESS_TOKEN**: Your Genius API access token. This token is used to fetch song lyrics and metadata.

### 3. [Last.fm API](https://www.last.fm/api)
- **LASTFM_API_KEY**: Your Last.fm API key. This key allows you to access user listening data and track information. Last.fm is used to search tracks by tag.

### 4. [Groq API](https://console.groq.com/docs/overview)
- **GROQ_API_KEY**: Your Groq API key. This key is used for integrating with Groq's AI services.

## Required Libraries
    python-dotenv
    pandas
    spotipy
    lyricsgenius
    langchain
    langchain-groq
    langgraph
    pydantic
    streamlit

All of these libraries are listed in the `requirements.txt` file. 


## Installation

Follow these steps to set up the project on your local machine:

### 1. Clone the repository


First, clone the repository to your local machine using the following command:

    git clone https://github.com/emrebayir1/hey-dj.git
    cd hey-dj

### 2. Generate the `.env` file

Create a `.env` file in the root directory of the project and add the necessary API keys. You can refer to the "Requirement API's" section to find out which keys are required. The `.env` file should look like this:

    SPOTIPY_CLIENT_ID=your_spotify_client_id
    SPOTIPY_CLIENT_SECRET=your_spotify_client_secret
    SPOTIPY_REDIRECT_URI=your_redirect_uri
    GENIUS_ACCESS_TOKEN=your_genius_access_token
    LASTFM_API_KEY=your_lastfm_api_key
    GROQ_API_KEY=your_groq_api_key

### 3. Install the required libraries

Once you have the `.env` file in place, install the required dependencies by running the following command:

    pip install -r requirements.txt

### 4. Run the Streamlit app

To start the app, run the following command:

    streamlit run main.py

### 5. Log in to Spotify

Once the app opens in your browser, you need to log in to your Spotify account via sidebar. Follow the instructions to authorize the app and gain access to your Spotify data.
