import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import pandas as pd

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
        self._user_data_save_path = os.getenv("USER_DATA_SAVE")
        # Check if api keys are available  
        if not self._spotify_client_id or not self._spotify_client_secret:
            raise ValueError("Spotify client ID and secret must be set in the environment variables.")
        # Authenticate with Spotify using OAuth2
        self._sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=self._spotify_client_id,
            client_secret=self._spotify_client_secret,
            redirect_uri=self._spotify_redirect_uri,
            scope=self._scope,
            cache_path= os.path.join(os.getenv("SPOTIFY_CACHE_PATH") , ".cache"),
            show_dialog=True
        ))
        #Private variables
        self._user_id = ""
        self._user_name = ""
        self._Playlists_Details = []
        self._current_playlist_content = []
        self._liked_playlist_content = []
        #Content_code mapping for liked content save or playlistdetails save or playlist content save
        self._content_code_map = {1: self._Playlists_Details, 2: self._current_playlist_content, 3: self._liked_playlist_content}
    def get_user_id(self):
        """
        Fetch the current authenticated user's Spotify user ID.

        Args:
            sp: Spotipy client object.

        Returns:
            str: The user's Spotify ID.
            str: The user's Spotify display name.
        """
        try:
            user_profile = self._sp.current_user()
            # print(f"\n user profile details from response: {user_profile}")
            user_id = user_profile.get('id')  
            user_name = user_profile.get('display_name')
            self._user_id = user_id
            self._user_name = user_name
            return self._user_id,self._user_name
        except Exception as e:
            print(f"Error fetching user ID: {e}")
            return None

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
            print("Token is valid.")
            print("USER INFORMATION\n")
            for i, (key, value) in enumerate(self._info_user.items(), start=1):
                print(f"\n{i}. {key} : {value}")
            return True
        except spotipy.exceptions.SpotifyException as e:
            if 'expired' in str(e).lower():
                print("Token is expired.")
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


    def get_list_of_playlist(self,limit = 20):
        """
        Fetch playlists of a specific Spotify user.

        Args:
            limit (int): Number of playlists to fetch per request.

        Returns:
            list: A list of playlists with names and IDs.
        """
        try:
            results = self._sp.user_playlists(user=self._user_id, limit=limit)
            playlists = [
                {'name': item['name'], 'id': item['id']}
                for item in results['items']
            ]
            self._Playlists_Details = playlists
            self._content_code_map[1] = self._Playlists_Details
            return "List_Of_Playlists",playlists
        except Exception as e:
            print(f"Error fetching user playlists: {e}")
            return "",[]

        
    def get_playlist_content(self, playlist_id):
            """
            Fetch the contents of a Spotify playlist by ID and return details like 
            song name, artist name, genre, and album name.
            
            Args:
                playlist_id (str): The Spotify playlist ID.

            Returns:
                list: A list of dictionaries containing song details.
            """
            try:
                if(self._Playlists_Details == []):
                    self.get_list_of_playlist()
                
                # Get the current user's playlists
                self._results = self._sp.playlist_items(playlist_id ,limit=100)

                # List to store the playlist content
                self._playlist_content = []
                self._playlist_name = ""
                
                for item in self._Playlists_Details:
                    if item['id'] == playlist_id:
                        self._playlist_name = item['name']
                        break
                
                while self._results:
                    for item in self._results['items']:
                        track = item['track']
                        #extract details from track 
                        song_name = track['name']
                        artist_name = track['artists'][0]['name']
                        artist_id = track['artists'][0]['id']
                        album_name = track['album']['name']
                        artist_info = self._sp.artist(artist_id)
                        genre = ', '.join(artist_info['genres']) if artist_info['genres'] else 'Unknown'
                        #get date added and date released
                        date_added = item['added_at']
                        release_date = track['album']['release_date']
                        #append details to self._playlist_content
                        self._playlist_content.append({
                            'song_name': song_name,
                            'artist_name': artist_name,
                            'artist_id': artist_id,
                            'genre': genre,
                            'album_name': album_name,
                            'date_released': release_date,
                            'date_added': date_added
                            })
                    # Get the next page of results if available
                    self._results = self._sp.next(self._results) if self._results['next'] else None
                self._current_playlist_content = self._playlist_content
                self._content_code_map[2] = self._current_playlist_content
                return self._playlist_name , self._playlist_content
            except Exception as e:
                print(f"Error fetching playlist content: {e}")
                return "",[]

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
                    song_name = track['name']
                    artist_name = track['artists'][0]['name']
                    artist_id = track['artists'][0]['id']
                    album_name = track['album']['name']
                    # Fetch artist details to get the genre
                    artist_info = self._sp.artist(artist_id)
                    genre = ', '.join(artist_info['genres']) if artist_info['genres'] else 'Unknown'
                    #get date added and date released
                    date_added = item['added_at']
                    release_date = track['album']['release_date']
                    # Append the details to the list
                    self._liked_songs_content.append({
                        'song_name': song_name,
                        'artist_name': artist_name,
                        'artist_id': artist_id,
                        'genre': genre,
                        'album_name': album_name,
                        'date_released': release_date,
                        'date_added': date_added
                    })

                # Fetch the next batch of results if available
                self._results = self._sp.next(self._results) if self._results['next'] else None
            self._liked_playlist_content = self._liked_songs_content
            self._content_code_map[3] = self._liked_playlist_content
            return "Liked_Songs",self._liked_songs_content

        except Exception as e:
            print(f"Error fetching liked songs: {e}")
            return "",[]
    
    def save_data_as_csv(self,save_name,content_code):
        #Get content according to content code
        content = self._content_code_map.get(content_code)
        # print(f"\ncontent: {content}")
        #check if content is empty
        if content is None:
            print(f"\nContent code: {content_code}")
            return False
        if not content:
            print(f"\nContent is empty: {content}")
            return False
        #Save content as csv 
        try:
            final_path = os.path.join(self._user_data_save_path,f"{save_name}.csv")
            df = pd.DataFrame(content)
            df.to_csv(final_path, index=False)
            print(f"Data saved successfully to {save_name}.csv")
            return True
        except Exception as e:
            print(f"Error saving data to CSV: {e}")
            return False
        
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
        
        print("/n",results)
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

