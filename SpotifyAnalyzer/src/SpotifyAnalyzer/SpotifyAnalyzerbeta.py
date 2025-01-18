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
        # Check if api keys are available  
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
        #Private variables 
        self._Playlist_Details = []
        self._current_playlist_content = []
        self._liked_playlist_content = []

    def check_token_validity(self):
        """
        Verifies the validity of the current Spotify API token.

        This method checks if the current token is valid by attempting to fetch
        the current user's details using the Spotify API. If the token is valid,
        it displays the user information. If the token is invalid or expired,
        the method handles the error by attempting reauthentication.

        Returns:
            bool: 
                - True if the token is valid.
                - False if the token is invalid or expired, and reauthentication is triggered.

        Exceptions:
            spotipy.exceptions.SpotifyException: Raised when the Spotify API returns an error.

        Behavior:
            - Prints "Token is valid." and the user's information if the token is valid.
            - Prints "Token is expired." and triggers reauthentication if the token has expired.
            - Prints "Token is invalid." and triggers reauthentication if the token is otherwise invalid.
        """
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


    def get_list_of_playlist(self):
        """
        Fetches a list of all playlists available to the authenticated user.
        
        Returns:
            list: A list of playlists with their names and IDs.
        """
        try:
            self._playlists = self._sp.current_user_playlists(limit=20)
            self._all_playlists = []
            # Loop through playlists and collect details
            while self._playlists:
                for playlist in self._playlists['items']:
                    self._all_playlists.append({
                        'name': playlist['name'],
                        'id': playlist['id']
                    })
                # Fetch the next set of playlists if available
                self._playlists = self._sp.next(self._playlists) if self._playlists['next'] else None
            #Assign to class variable
            self._Playlist_Details =self._all_playlists
            # print(self._Playlist_Details)
            return self._all_playlists
        except Exception as e:
            print(f"Error fetching playlists: {e}")
            return []

    def get_playlist_content(self , playlist_id):
        """
        Fetch the contents of a Spotify playlist by ID and return details like 
        song name, artist name, genre, and album name.
        
        Args:
            playlist_id (str): The Spotify playlist ID.

        Returns:
            list: A list of dictionaries containing song details.
        """
        try:
            self._results = self._sp.playlist_items(playlist_id, additional_types=('track',))
            self._playlist_content = []

            while self._results:
                for item in self._results['items']:
                    track = item['track']
                    #extract details from track 
                    self._song_name = track['name']
                    self._artist_name = track['artists'][0]['name']
                    self._artist_id = track['artists'][0]['id']
                    self._album_name = track['album']['name']
                    self._artist_info = self._sp.artist(self._artist_id)
                    self._genre = ', '.join(self._artist_info['genres']) if self._artist_info['genres'] else 'Unknown'
                    #append details to self._playlist_content
                    self._playlist_content.append({
                        'song_name': self._song_name,
                        'artist_name': self._artist_name,
                        'artist_id': self._artist_id,
                        'genre': self._genre,
                        'album_name': self._album_name
                        })
                # Get the next page of results if available
                self._results = self._sp.next(self._results) if self._results['next'] else None

            self._current_playlist_content = self._playlist_content
            #print(self._current_playlist_content)
            return self._playlist_content
        except Exception as e:
            print(f"Error fetching playlist content: {e}")
            return []

    def get_liked_songs_playlist(self):
        """
        Fetch the authenticated user's liked songs and return details like
        song name, artist name, genre, and album name in the desired structure.

        Returns:
            list: A list of dictionaries containing song details.
        """
        try:
            # Initialize the list to hold the liked song details
            self._liked_songs_content = []
            self._results = self._sp.current_user_saved_tracks(limit=50)  # Fetch initial batch of liked songs

            while self._results:
                for item in self._results['items']:
                    track = item['track']
                    # Extract details from the track
                    self._song_name = track['name']
                    self._artist_name = track['artists'][0]['name']
                    self._artist_id = track['artists'][0]['id']
                    self._album_name = track['album']['name']
                    # Fetch artist details to get the genre
                    self._artist_info = self._sp.artist(self._artist_id)
                    self._genre = ', '.join(self._artist_info['genres']) if self._artist_info['genres'] else 'Unknown'
                    # Append the details to the list
                    self._liked_songs_content.append({
                        'song_name': self._song_name,
                        'artist_name': self._artist_name,
                        'artist_id': self._artist_id,
                        'genre': self._genre,
                        'album_name': self._album_name
                    })

                # Fetch the next batch of results if available
                self._results = self._sp.next(self._results) if self._results['next'] else None
            self._liked_playlist_content = self._liked_songs_content
            return self._liked_songs_content

        except Exception as e:
            print(f"Error fetching liked songs: {e}")
            return []
    

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




