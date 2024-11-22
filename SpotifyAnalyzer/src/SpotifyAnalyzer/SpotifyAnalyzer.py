import shutil
import logging
import os
import spotipy
import requests
import time
import webbrowser
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

#load environment variables
load_dotenv(dotenv_path= ".env.api" , override=True)
load_dotenv(dotenv_path= ".env.path" , override=True)


class SpotifyAnalysis:
    def __init__(self):
        self._spotify_client_id = os.getenv("SPOTIFY_CLIENT_ID")
        self._spotify_client_id_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        self._cache_dir = os.getenv("SPOTIFY_CACHE_PATH", "SpotifyAnalyzer/src")
        self._redirect_uri = "https://spotifystudio.github.io/SpotifyAnalyzer/"
        self._scope = "user-top-read"
        # Ensure the cache directory exists
        if not os.path.exists(self._cache_dir):
            os.makedirs(self._cache_dir)
        #initialize the user
        self._sp = self._initialize_spotify_client()
    def Check_spotify_api_limit(self):
        token_info = self._sp.auth_manager.get_access_token(as_dict=True)
        headers = {"Authorization": f"Bearer {token_info['access_token']}"}
        response = requests.get("https://api.spotify.com/v1/me/playlists", headers=headers)
        if response.ok:
            print("API Request Successful!")
            #print(f"Headers: {response.headers}")
        elif response.status_code == 429:
            retry_after = response.headers.get("Retry-After", 1)
            print(f"Rate limit exceeded. Retrying after {retry_after} seconds.")
            time.sleep(int(retry_after))
            self.Check_spotify_api_limit()
        else:
            print(f"API Request Failed: {response.status_code} - {response.reason}")
        
    def _initialize_spotify_client(self):
        cache_path = os.path.join(self._cache_dir, "user_cache")
        auth_manager = SpotifyOAuth(
            client_id=self._spotify_client_id,
            client_secret=self._spotify_client_id_secret,
            redirect_uri=self._redirect_uri,
            scope=self._scope,
            cache_path=cache_path
        )
        # Get the authorization URL and open it in a browser
        auth_url = auth_manager.get_authorize_url()
        print(f"Please go to the following URL to authorize the application: {auth_url}")
        webbrowser.open(auth_url)  # Opens the URL in the default web browser
        
        # After user grants permissions, get the access token
        token_info = auth_manager.get_access_token(input("Paste the URL you were redirected to: "), as_dict=True)
        
        return spotipy.Spotify(auth_manager=auth_manager)
    def get_top_songs_of_artist(self,artist_name):
        # Search for the artist
        #list of top songs by artist
        artist_top_songs = []
        results = self._sp.search(q=artist_name, type="artist", limit=1)
        
        if not results['artists']['items']:
            print(f"No artist found for '{artist_name}'")
            return
        
        artist = results['artists']['items'][0]
        artist_id = artist['id']
        artist_name = artist['name']
        
        #print(f"Artist Found: {artist_name} (ID: {artist_id})")
        
        # Get top tracks
        top_tracks = self._sp.artist_top_tracks(artist_id)
        
        #print(f"\nTop Tracks for {artist_name}:")
        for idx, track in enumerate(top_tracks['tracks'], start=1):
            #print(f"{idx}. {track['name']} - {track['popularity']} popularity")
            artist_top_songs.append([idx, track["name"] , track["popularity"]])
        return artist_top_songs
    def get_user_top_tracks(self):
        # Fetch top tracks of the user
        results = self._sp.current_user_top_tracks(limit=10, time_range="medium_term")  # Top tracks in last 6 months
        user_top_tracks = []

        for idx, track in enumerate(results['items'], start=1):
            # Append track name and artist to the list
            user_top_tracks.append(f"{idx}. {track['name']} by {', '.join(artist['name'] for artist in track['artists'])}")
        
        return user_top_tracks