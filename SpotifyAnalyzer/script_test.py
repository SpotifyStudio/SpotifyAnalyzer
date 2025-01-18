import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env.api")

client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")
def Spotify():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope="playlist-read-private playlist-read-collaborative",
        cache_path=None,
        show_dialog=True
    ))
    return sp
sp = Spotify()
user_info = sp.current_user()
print("Current user detail:\n\n",user_info)
playlist = sp.current_user_playlists(limit= 20)

print("Playlist response :\n\n",playlist)