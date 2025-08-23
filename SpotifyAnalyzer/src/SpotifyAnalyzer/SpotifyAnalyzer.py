import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import pandas as pd

# Load environment variables
load_dotenv(dotenv_path=".env.api", override=True)
load_dotenv(dotenv_path=".env.path", override=True)

class SpotifyAnalysis:
    """
    A class for analyzing a user's Spotify account by retrieving and managing playlist 
    and song data using the Spotify API.

    This class:
    - Authenticates the user via Spotify OAuth.
    - Fetches user details, playlists, and playlist content.
    - Verifies and refreshes authentication tokens.
    - Stores and organizes data in structured formats.

    Features:
    - Retrieve user ID and display name.
    - Validate API token and reauthenticate if necessary.
    - Fetch playlists and their details.
    - Retrieve song information from playlists.
    - Maintain a structured mapping of fetched content.

    Raises:
        ValueError: If API credentials are missing from environment variables.

    Example Usage:
        >>> spotify = SpotifyAnalysis()
        >>> spotify.get_user_id()
        ('user123', 'John Doe')
        >>> playlists = spotify.get_list_of_playlist()
    """
    def __init__(self):
        """
        Initializes the Spotify API client and sets up user authentication.

        This constructor:
        - Loads Spotify API credentials from environment variables.
        - Authenticates the user using OAuth2.
        - Initializes private variables to store user and playlist data.
        - Defines a mapping for different types of content storage.

        Parameters:
            None (Values are fetched from environment variables)

        Returns:
            None

        Instance Variables:
            - self._spotify_client_id (str): Spotify API Client ID loaded from environment variables.
            - self._spotify_client_secret (str): Spotify API Client Secret loaded from environment variables.
            - self._spotify_redirect_uri (str): Redirect URI for OAuth authentication.
            - self._scope (str): Permissions required for accessing Spotify data.
            - self._user_data_save_path (str): Path to save user data, fetched from environment variables.
            - self._sp (Spotify): Authenticated Spotify API client instance.
            - self._user_id (str): Stores the user’s unique Spotify ID.
            - self._user_name (str): Stores the user’s Spotify display name.
            - self._Playlists_Details (list): Stores details of the user's playlists.
            - self._current_playlist_content (list): Stores tracks of the currently selected playlist.
            - self._liked_playlist_content (list): Stores tracks from the user's liked songs.

        Content Code Map:
        
        self._content_code_map (dict): A mapping of integer codes to content storage variables.
            - 1 → self._Playlists_Details (User's playlists details)
            - 2 → self._current_playlist_content (Currently selected playlist's content)
            - 3 → self._liked_playlist_content (User's liked songs)

        Raises:
            ValueError: If Spotify Client ID or Client Secret is not set in environment variables.

        Example:
            >>> obj = SpotifyClient()
            Spotify authentication successful.

        Notes:
            - The `cache_path` stores authentication tokens to prevent frequent re-authentication.
            - `show_dialog=True` forces login prompt for user authorization.
        """
        # Load credentials from environment variables
        self._spotify_client_id = os.getenv("SPOTIFY_CLIENT_ID")
        self._spotify_client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        self._spotify_redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")
        self._scope = "user-top-read user-read-recently-played user-library-read playlist-read-private playlist-read-collaborative"
        self._user_data_save_path = os.getenv("SPOTIFY_USER_DATA_SAVE_PATH")
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
        ### DESCRIPTION
        
        Fetch the current authenticated user's Spotify user ID and display name.

        ### PARAMETERS
        None

        ### RETURN
        
        - user_id (str): The user's Spotify ID.
        - user_name (str): The user's Spotify display name.
        - None: Returns None if an error occurs while fetching the user details.
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
        ### DESCRIPTION
        
        Verifies the validity of the current Spotify API token.

        ### PARAMETERS
        
        None

        ### RETURN
        
        is_valid (bool):
            - True if the token is valid.
            - False if the token is invalid or expired, triggering reauthentication.
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
        """
        ### DESCRIPTION
        
        Prompts the user to authenticate again and updates the Spotify API token.

        ### PARAMETERS
        
        None

        ### RETURN
        
        None

        ### BEHAVIOR
        
        - Initiates the authentication process using SpotifyOAuth.
        - Updates the authentication manager with a new token.
        - Prints "Authentication successful. Token updated." upon success.
        """
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
    

    def get_list_of_playlist(self, limit = 20):
        """
        ### DESCRIPTION
        
        Fetches the playlists of the authenticated Spotify user.

        ### PARAMETERS
        
        limit (int): The number of playlists to fetch per request (default is 20).

        ### RETURN

        list_of_playlists (str): A label indicating the returned data.
        playlists (list of dict): A list of dictionaries, where each dictionary represents a playlist with:
            - 'name' (str): The name of the playlist.
            - 'id' (str): The unique identifier of the playlist.

            Example:
            [
                {"name": "Playlist 1", "id": "12345abcde"},
                {"name": "Playlist 2", "id": "67890fghij"},
                ...
            ]

        If an error occurs, returns an empty string and an empty list.

        ### BEHAVIOR
        - Retrieves the user's playlists using the Spotify API.
        - Stores playlist details in `_Playlists_Details` and `_content_code_map[1]`.
        - Returns the list of playlists along with a label.
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
        ### DESCRIPTION
        
        Fetches the contents of a Spotify playlist using its playlist ID. 
        Returns details such as song name, artist name, genre, and album name.

        ### PARAMETERS
        
        playlist_id (str): The unique Spotify ID of the playlist.

        ### RETURN
        
        playlist_name (str): The name of the playlist.
        playlist_content (list of dict): A list of dictionaries where each dictionary represents a song with:
        
            - 'song_name' (str): Name of the song.
            - 'song_id' (str): Unique ID of the song.
            - 'artist_name' (str): Name of the primary artist.
            - 'artist_id' (str): Unique ID of the artist.
            - 'genre' (str): Genre(s) associated with the artist.
            - 'album_name' (str): Name of the album the song belongs to.
            - 'date_released' (str): Release date of the song.
            - 'date_added' (str): Date when the song was added to the playlist.
            - "popularity" (int): A score of how popular the song is on spotify.

            Example:
            
            [
                {
                    "song_name": "Blinding Lights",
                    "song_id": "3A2gZZ3j5ZSU2hE2p9Ddlg",
                    "artist_name": "The Weeknd",
                    "artist_id": "1Xyo4u8uXC1ZmMpatF05PJ",
                    "genre": "R&B, Pop",
                    "album_name": "After Hours",
                    "date_released": "2020-03-20",
                    "date_added": "2023-07-15T12:34:56Z",
                    "popularity": 90
                },
                {
                    "song_name": "Shape of You",
                    "song_id": "7qiZfU4dY1lWllzX7mPBI3",
                    "artist_name": "Ed Sheeran",
                    "artist_id": "6eUKZXaKkcviH0Ku9w2n3V",
                    "genre": "Pop",
                    "album_name": "Divide",
                    "date_released": "2017-01-06",
                    "date_added": "2023-07-16T08:20:30Z",
                    "popularity": 94
                },
                ...
            ]

        If an error occurs, returns an empty string and an empty list.

        ### BEHAVIOR
        
        - If the playlist details are not already fetched, it retrieves them using `get_list_of_playlist()`.
        - Fetches up to 100 songs per request and continues paginated requests if more songs are available.
        - Stores playlist details in `_current_playlist_content` and `_content_code_map[2]`.
        - Returns the playlist name along with the list of song details.
        """
        try:
            if not self._Playlists_Details:
                self.get_list_of_playlist()

            # Get the playlist items (first page)
            results = self._sp.playlist_items(playlist_id, limit=100)

            # Prepare list to store playlist content
            self._playlist_content = []
            self._playlist_name = ""

            # Find the playlist name from stored details
            for item in self._Playlists_Details:
                if item['id'] == playlist_id:
                    self._playlist_name = item['name']
                    break

            # Paginate through all playlist items
            while results:
                for item in results['items']:
                    track = item['track']
                    if not track:  # Skip if no track data
                        continue
                    self._playlist_content.append({
                        'song_name': track['name'],
                        'song_id': track['id'],
                        'artist_name': track['artists'][0]['name'],
                        'artist_id': track['artists'][0]['id'],
                        'genre': None,  # placeholder for batch fill
                        'album_name': track['album']['name'],
                        'date_released': track['album']['release_date'],
                        'date_added': item['added_at'],
                        'popularity': track['popularity']
                    })
                results = self._sp.next(results) if results['next'] else None

            # ✅ Get all unique artist IDs
            artist_ids = list({t['artist_id'] for t in self._playlist_content})

            # ✅ Batch fetch genres (max 50 IDs per API call)
            artist_genres = {}
            for i in range(0, len(artist_ids), 50):
                batch = artist_ids[i:i+50]
                artists_info = self._sp.artists(batch)
                for a in artists_info['artists']:
                    artist_genres[a['id']] = ', '.join(a['genres']) if a['genres'] else 'Unknown'

            # ✅ Fill genres back into playlist content
            for track in self._playlist_content:
                track['genre'] = artist_genres.get(track['artist_id'], 'Unknown')

            self._current_playlist_content = self._playlist_content
            self._content_code_map[2] = self._current_playlist_content
            return self._playlist_name, self._playlist_content

        except Exception as e:
            print(f"Error fetching playlist content: {e}")
            return "", []
    

    def get_liked_songs_playlist(self):
        """
        ### DESCRIPTION
        
        Fetches the authenticated user's liked songs and returns details such as 
        song name, artist name, genre, album name, and additional metadata.
            
        ### RETURN
        
        liked_songs_label (str): A label indicating the returned data ("Liked_Songs").
        liked_songs_content (list of dict): A list of dictionaries where each dictionary represents a liked song with:
        
            - 'song_name' (str): Name of the song.
            - 'song_url' (str): Unique ID (URL) of the song.
            - 'artist_name' (str): Name of the primary artist.
            - 'artist_id' (str): Unique ID of the artist.
            - 'genre' (str): Genre(s) associated with the artist.
            - 'album_name' (str): Name of the album the song belongs to.
            - 'date_released' (str): Release date of the song.
            - 'date_added' (str): Date when the song was liked.
            - "popularity" (int): A score of how popular the song is on spotify.
            
            Example:
            [
                {
                    "song_name": "Blinding Lights",
                    "song_url": "3A2gZZ3j5ZSU2hE2p9Ddlg",
                    "artist_name": "The Weeknd",
                    "artist_id": "1Xyo4u8uXC1ZmMpatF05PJ",
                    "genre": "R&B, Pop",
                    "album_name": "After Hours",
                    "date_released": "2020-03-20",
                    "date_added": "2023-07-15T12:34:56Z",
                    "popularity": 90
                },
                {
                    "song_name": "Shape of You",
                    "song_url": "7qiZfU4dY1lWllzX7mPBI3",
                    "artist_name": "Ed Sheeran",
                    "artist_id": "6eUKZXaKkcviH0Ku9w2n3V",
                    "genre": "Pop",
                    "album_name": "Divide",
                    "date_released": "2017-01-06",
                    "date_added": "2023-07-16T08:20:30Z",
                    "popularity": 95
                },
                ...
            ]

        If an error occurs, returns an empty string and an empty list.

        ### BEHAVIOR
        
        - Fetches the user's liked songs in batches of 50.
        - Iterates through the pages until all liked songs are retrieved.
        - Extracts relevant metadata, including song name, artist, genre, album, and timestamps.
        - Stores the liked songs' details in `_liked_playlist_content` and `_content_code_map[3]`.
        - Returns a label along with the structured list of liked songs.
        """
        try:
            # Initialize the list to hold the liked song details
            self._liked_songs_content = []

            results = self._sp.current_user_saved_tracks(limit=50)  # Fetch initial batch of liked songs

            while results:
                for item in results['items']:
                    track = item['track']
                    if not track:
                        continue

                    self._liked_songs_content.append({
                        'song_name': track['name'],
                        'song_id': track['id'],
                        'artist_name': track['artists'][0]['name'],
                        'artist_id': track['artists'][0]['id'],
                        'genre': None,  # placeholder for later batch filling
                        'album_name': track['album']['name'],
                        'date_released': track['album']['release_date'],
                        'date_added': item['added_at'],
                        'popularity': track['popularity']
                    })

                # Fetch the next batch of results if available
                results = self._sp.next(results) if results['next'] else None

            # Batch fetch genres for all unique artists (max 50 per call)
            artist_ids = list({t['artist_id'] for t in self._liked_songs_content})
            artist_genres = {}
            for i in range(0, len(artist_ids), 50):
                batch = artist_ids[i:i+50]
                artists_info = self._sp.artists(batch)
                for a in artists_info['artists']:
                    artist_genres[a['id']] = ', '.join(a['genres']) if a['genres'] else 'Unknown'

            # Fill the genre field for each song
            for t in self._liked_songs_content:
                t['genre'] = artist_genres.get(t['artist_id'], 'Unknown')

            self._liked_playlist_content = self._liked_songs_content
            self._content_code_map[3] = self._liked_playlist_content
            return "Liked_Songs", self._liked_songs_content

        except Exception as e:
            print(f"Error fetching liked songs: {e}")
            return "", []
    

    def save_data_as_csv(self, save_name,content_code):
        """
        ### DESCRIPTION
        
        Saves the provided content (list of dictionaries) as a CSV file.

        ### PARAMETERS
        
        save_name (str): The desired filename (without extension) for saving the CSV.
        content_code (int): The code representing the stored content in `_content_code_map`.

        ### RETURN
        
        success (bool): 
            - True if the data is successfully saved as a CSV.
            - False if the content is missing, empty, or an error occurs.

        ### BEHAVIOR
        
        - Retrieves the content corresponding to `content_code` from `_content_code_map`.
        - Checks if the content exists and is non-empty.
        - Converts the content (list of dictionaries) into a Pandas DataFrame.
        - Saves the DataFrame as a CSV file in `_user_data_save_path` with `save_name`.
        - Handles exceptions and logs errors.

        ### EXPECTED CONTENT STRUCTURE (list of dict)
        
        The content should be a list of dictionaries, where each dictionary represents 
        a row in the CSV file. Example structure:

        [
            {
                "song_name": "Blinding Lights",
                "song_id": "3A2gZZ3j5ZSU2hE2p9Ddlg",
                "artist_name": "The Weeknd",
                "artist_id": "1Xyo4u8uXC1ZmMpatF05PJ",
                "genre": "R&B, Pop",
                "album_name": "After Hours",
                "date_released": "2020-03-20",
                "date_added": "2023-07-15T12:34:56Z",
                "popularity": 90
            },
            {
                "song_name": "Shape of You",
                "song_id": "7qiZfU4dY1lWllzX7mPBI3",
                "artist_name": "Ed Sheeran",
                "artist_id": "6eUKZXaKkcviH0Ku9w2n3V",
                "genre": "Pop",
                "album_name": "Divide",
                "date_released": "2017-01-06",
                "date_added": "2023-07-16T08:20:30Z",
                "popularity": 90
            },
            ...
        ]

        ### NOTES
        
        - If the `content_code` does not exist in `_content_code_map`, the function returns `False`.
        - If the content is an empty list, a message is printed and the function returns `False`.
        - The CSV file is saved without an index.
        """
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
        
        #print("/n",results)
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
    

    def get_track_metrics(self, content_code):
        try:
            playlist = self._content_code_map[content_code]
            if not playlist:
                print("No playlist/tracks found for the given content code.")
                return []
            # extract all track ids into track_ids
            track_ids = [track['song_id'] for track in playlist if track.get('song_id')]
            # if no track found 
            if not track_ids:
                print("No valid track IDs found.")
                return playlist
            # prepare audio_feature_map
            audio_features_map = dict()
            # get audio features in batches of 100 max
            for i in range(0, len(track_ids), 100):
                batch = track_ids[i:i+100]
                features_list = self._sp.audio_features(batch)
                for f in features_list:
                    if f and f.get('id'):
                        audio_features_map[f['id']] = f
            print(audio_features_map)
            
            
        except Exception as e:
            print(f"Error in fetching track metrics: {e}");
            return [];
    

    def logout_user(self):
        """
        ### DESCRIPTION
        Logs out the current authenticated Spotify user by:
        - Clearing the authentication token cache.
        - Deleting user data files.
        - Resetting the `self._sp` instance.

        ### PARAMETERS
        None

        ### RETURN
        None

        ### BEHAVIOR
        - **Removes Spotify authentication cache**:  
        - Deletes all files in the cache directory (`SPOTIFY_CACHE_PATH`), keeping the folder intact.
        - If no cache exists, a message is displayed.
        
        - **Resets the Spotify API instance (`self._sp`)**:  
        - Prevents further API calls after logout.
        
        - **Deletes user data files**:  
        - Removes all files inside `self._user_data_save_path` but **keeps the directory** intact.
        - Ensures only files are deleted, avoiding unintended folder removal.
        
        - **Handles errors gracefully**:  
        - Catches and prints any exceptions that occur during the logout process.
        """
        try:
            # Remove Spotify cache files but keep the directory
            cache_path = os.getenv("SPOTIFY_CACHE_PATH")
            if cache_path and os.path.exists(cache_path):
                for file in os.listdir(cache_path):
                    file_path = os.path.join(cache_path, file)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                print("Spotify cache cleared.")
            else:
                print("No Spotify cache found.")
            # Reassign sp to None
            self._sp = None
            # Delete only files inside user data folder but keep the folder
            if os.path.exists(self._user_data_save_path):
                for file in os.listdir(self._user_data_save_path):
                    file_path = os.path.join(self._user_data_save_path, file)
                    if os.path.isfile(file_path):  # Ensure only files are deleted
                        os.remove(file_path)
                print("User data files deleted.")
        except Exception as e:
            print(f"Error logging out: {e}")
    

