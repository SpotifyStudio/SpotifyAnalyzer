import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=".env.api", override=True)
load_dotenv(dotenv_path=".env.path", override=True)


class SpotifyAnalysis:
    def __init__(self):
        # Load credentials from environment variables
        self._spotify_client_id = os.getenv("SPOTIFY_CLIENT_ID")
        self._spotify_client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        self._spotify_redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")
        self._scope = "user-top-read user-read-recently-played user-library-read playlist-read-private playlist-read-collaborative"

        if not self._spotify_client_id or not self._spotify_client_secret:
            raise ValueError("Spotify client ID and secret must be set in the environment variables.")

        # Authenticate with Spotify using OAuth2
        self._sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=self._spotify_client_id,
            client_secret=self._spotify_client_secret,
            redirect_uri=self._spotify_redirect_uri,
            scope=self._scope,
            cache_path= os.path.join(os.getenv("SPOTIFY_CACHE_PATH") , ".cache")
        ))

    def check_token_validity(self):
        """Check if token is valid"""
        try:
            # Try to get the current user details
            self._info_user = self._sp.current_user()
            print(f"Token is valid.")
            print("USER INFORMATION\n")
            for i, (key, value) in enumerate(self._info_user.items(), start=1):
                print(f"\n{i}. {key} : {value}")
            return True
        except spotipy.exceptions.SpotifyException as e:
            if 'expired' in str(e).lower():
                print("Token is expired.")
                self.Reauthenticate()
            else:
                print("Token is invalid.")
                self.Reauthenticate()
            return False
        

    def Reauthenticate(self):
        """Prompt user to authenticate again and save new token."""
        print("Starting authentication process...")
        self._sp.auth_manager = SpotifyOAuth(
            client_id=self._spotify_client_id,
            client_secret=self._spotify_client_secret,
            redirect_uri=self._spotify_redirect_uri,
            scope=self._scope,
            cache_path=os.path.join(os.getenv("SPOTIFY_CACHE_PATH"), ".cache")
        )
        # Get the new access token and update the _sp instance
        self._sp = spotipy.Spotify(auth_manager=self._sp.auth_manager)
        print("Authentication successful. Token updated.")

    def get_artist_top_tracks(self, artist_name):
        """
        Fetches and displays the top tracks of a given artist.
        
        Parameters:
            artist_name (str): Name of the artist.
        
        Returns:
            list: A list of tuples containing track names and their popularity.
        """
        # Search for the artist
        results = self._sp.search(q=f"artist:{artist_name}", type='artist', limit=1)
        if not results['artists']['items']:
            return f"No artist found with the name '{artist_name}'"

        artist = results['artists']['items'][0]
        artist_id = artist['id']
        print(f"Found Artist: {artist['name']} (ID: {artist_id})")

        # Get the artist's top tracks
        tracks = self._sp.artist_top_tracks(artist_id)
        top_tracks = [(track['name'], track['popularity']) for track in tracks['tracks']]

        # Display the top tracks
        for i, (name, popularity) in enumerate(top_tracks, start=1):
            print(f"{i}. {name} (Popularity: {popularity})")

        return top_tracks

