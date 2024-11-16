import shutil
import logging
import os
import spotipy
import requests
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

#load environment variables
load_dotenv(dotenv_path= ".env.api" , override=True)

class SpotifyAnalysis:
    def __init__(self):
        self._spotify_client_id = os.getenv("SPOTIFY_CLIENT_ID")
        self._spotify_client_id_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        #print(f"Spotify api id : {self._spotify_client_id}\nspotify client id secret : {self._spotify_client_id_secret}")
        self._sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id= self._spotify_client_id,
            client_secret = self._spotify_client_id_secret,
            redirect_uri = "http://example.com",
            scope="user-read-private"
        ))
    def Check_spotify_api_limit(self):
        headers = {"Authorization": f"Bearer {self._sp.auth_manager.get_access_token(as_dict=False)}"}
        response = requests.get("https://api.spotify.com/v1/me/playlists", headers=headers)
        
        if response.ok:
            print("API Request Successful!")
            print(f"Headers: {response.headers}")
        elif response.status_code == 429:
            retry_after = response.headers.get("Retry-After", 1)
            print(f"Rate limit exceeded. Retrying after {retry_after} seconds.")
            time.sleep(int(retry_after))
            self.Check_spotify_api_limit()
        else:
            print(f"API Request Failed: {response.status_code} - {response.reason}")
        
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