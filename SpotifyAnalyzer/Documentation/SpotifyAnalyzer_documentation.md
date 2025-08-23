# SpotifyAnalyzer - SpotifyAnalysis.py Documentation

## Overview

The `SpotifyAnalysis.py` file in the SpotifyAnalyzer project provides functionality to analyze a user's Spotify account by retrieving and managing playlist and song data using the Spotify API. This class is responsible for authenticating users, fetching their playlists and song details, and structuring the retrieved data for further analysis.

It includes features such as:
- Authenticating users via Spotify OAuth.
- Fetching user details, playlists, and playlist content.
- Validating API tokens and refreshing authentication if necessary.
- Organizing fetched data into structured formats for easy access.

These functionalities make `SpotifyAnalysis.py` an essential component of the SpotifyAnalyzer project, ensuring seamless interaction with the Spotify API.

---

## Table of Contents

- [Classes](#classes)  
  - [SpotifyAnalysis](#spotifyanalysis)  
- [Methods](#Methods)  
  - [**init**(self)](#initself)  
  - [get_user_id(self)](#get_user_idself)  
  - [check_token_validity(self)](#check_token_validityself)  
  - [Reauthenticate(self)](#reauthenticateself)  
  - [get_list_of_playlist(self, limit=20)](#get_list_of_playlistself-limit20)  
  - [get_playlist_content(self, playlist_id)](#get_playlist_contentself-playlist_id)  
  - [get_liked_songs_playlist(self)](#get_liked_songs_playlistself)  
  - [save_data_as_csv(self, save_name, content_code)](#save_data_as_csvself-save_name-content_code)  
  - [get_artist_top_tracks(self, artist_name)](#get_artist_top_tracksself-artist_name)  
  - [logout_user(self)](#logout_userself)  
- [Usage Example](#usage-example)  

---

## Classes

### SpotifyAnalysis

- **Description**:
    The `SpotifyAnalysis` class is responsible for analyzing a user's Spotify account by retrieving and managing playlist and song data using the Spotify API. It handles authentication, playlist retrieval, token management, and data organization in a structured manner.

- **Features**:
    - Authenticate users via Spotify OAuth.
    - Retrieve user ID and display name.
    - Validate and refresh authentication tokens.
    - Fetch playlists and their details.
    - Retrieve song information from playlists.
    - Maintain a structured mapping of fetched content.

- **Exceptions**:
    - `ValueError`: Raised if API credentials are missing from environment variables.  

---

## Methods

---

#### `__init__(self)`

- **Description**:  
    Initializes the `SpotifyAnalysis` class by setting up authentication with the Spotify API and preparing the instance for retrieving and   managing user data.

- **Input**:  
    - None (values are fetched from environment variables).

- **Output**:  
    - Initializes the `SpotifyAnalysis` object and sets up authentication.

- **Instance Variables**:  
    - `self._spotify_client_id` (str): Spotify API Client ID loaded from environment variables.  
    - `self._spotify_client_secret` (str): Spotify API Client Secret loaded from environment variables.  
    - `self._spotify_redirect_uri` (str): Redirect URI for OAuth authentication.  
    - `self._scope` (str): Required permissions for accessing Spotify data.  
    - `self._user_data_save_path` (str): Path to save user data.  
    - `self._sp` (Spotify): Authenticated Spotify API client instance.  
    - `self._user_id` (str): Stores the user’s unique Spotify ID.  
    - `self._user_name` (str): Stores the user’s Spotify display name.  
    - `self._Playlists_Details` (list): Stores details of the user’s playlists.  
    - `self._current_playlist_content` (list): Stores tracks of the currently selected playlist.  
    - `self._liked_playlist_content` (list): Stores tracks from the user’s liked songs.  

- **Content Code Mapping**:  
    A dictionary mapping integer codes to content storage variables:
        - `1 → self._Playlists_Details` (User's playlists details).  
        - `2 → self._current_playlist_content` (Currently selected playlist's content).  
        - `3 → self._liked_playlist_content` (User's liked songs).  

---

#### `get_user_id(self)`

- **Description**:  
    Retrieves the currently authenticated user's Spotify user ID and display name.

- **Input**:  
    - None

- **Output**:  
    - Returns a tuple containing:
        - `user_id` (str): The user's unique Spotify ID.  
        - `user_name` (str): The user's Spotify display name.  
    - Returns `None` if an error occurs while fetching user details.

---

#### `check_token_validity(self)`

- **Description**:  
    Verifies whether the current Spotify API token is valid. If the token is expired or invalid, it triggers reauthentication.

- **Input**:  
    - None

- **Output**:  
    - Returns `True` if the token is valid.  
    - Returns `False` if the token is expired or invalid, and automatically attempts reauthentication.

---

#### `Reauthenticate(self)`

- **Description**:  
    Prompts the user to reauthenticate with Spotify and updates the API token.

- **Input**:  
  - None  

- **Output**:  
  - None  

- **Behavior**:  
    - Re-initiates authentication using `SpotifyOAuth`.
    - Updates the authentication manager with a new token.
    - Replaces the existing Spotify API client instance with the newly authenticated session.
    - Prints `"Authentication successful. Token updated."` upon success.

---

#### `get_list_of_playlist(self, limit=20)`

- **Description**:  
    Fetches and returns the playlists of the authenticated Spotify user.

- **Input**:  
    - `limit` (int, optional): The number of playlists to fetch per request (default is 20).

- **Output**:  
    - **Label** (`str`): `"List_Of_Playlists"` indicating the type of returned data.
    - **Playlists** (`list of dict`): A list of dictionaries, where each dictionary represents a playlist.

- **Dictionary Structure** (Each Playlist Contains):  
    - `'name'` (`str`): The name of the playlist.
    - `'id'` (`str`): The unique identifier of the playlist.

- **List of Dictionaries Output:**
    ```json
    [
        {"name": "My Favorite Songs", "id": "3FvDkjskH5l"},
        {"name": "Chill Vibes", "id": "8hHdYtB24zA"},
        {"name": "Workout Hits", "id": "9KlsM3rA76P"}
    ]

---

#### `get_playlist_content(self, playlist_id)`

- **Description**:  
    Fetches the contents of a Spotify playlist using its playlist ID.  
    Returns details such as song name, artist name, genre, album name, release date, and popularity.

- **Input**:  
    - `playlist_id` (`str`): The unique Spotify ID of the playlist.

- **Output**:  
    - **Playlist Name** (`str`): The name of the playlist.
    - **Playlist Content** (`list of dict`): A list of dictionaries where each dictionary represents a song.

- **Dictionary Structure** (Each Song Contains):  
    - `'song_name'` (`str`): Name of the song.
    - `'song_id'` (`str`): Unique ID of the song.
    - `'artist_name'` (`str`): Name of the primary artist.
    - `'artist_id'` (`str`): Unique ID of the artist.
    - `'genre'` (`str`): Genre(s) associated with the artist.
    - `'album_name'` (`str`): Name of the album the song belongs to.
    - `'date_released'` (`str`): Release date of the song.
    - `'date_added'` (`str`): Date when the song was added to the playlist.
    - `'popularity'` (`int`): Popularity score of the song on Spotify.

- **Example Output:**
    ```json
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
        }
    ]

---

#### `get_liked_songs_playlist(self)`

- **Description**:  
    Fetches the contents of a Spotify Liked songs playlist.  
    Returns details such as song name, artist name, genre, album name, release date, and popularity.

- **Input**:  
    - `None`

- **Output**:  
    - **Liked_Songs** (`str`): The name of the playlist.
    - **Playlist Content** (`list of dict`): A list of dictionaries where each dictionary represents a song.

- **Dictionary Structure** (Each Song Contains):  
    - `'song_name'` (`str`): Name of the song.
    - `'song_id'` (`str`): Unique ID of the song.
    - `'artist_name'` (`str`): Name of the primary artist.
    - `'artist_id'` (`str`): Unique ID of the artist.
    - `'genre'` (`str`): Genre(s) associated with the artist.
    - `'album_name'` (`str`): Name of the album the song belongs to.
    - `'date_released'` (`str`): Release date of the song.
    - `'date_added'` (`str`): Date when the song was added to the playlist.
    - `'popularity'` (`int`): Popularity score of the song on Spotify.

  **Example Output:**
    ```json
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
        }
    ]

---

#### `save_data_as_csv(self,save_name,content_code)`

- **Description**:
    This function saves the provided content (a list of dictionaries) as a CSV file.

- **Input**:
    - `save_name` (str): The desired filename (without extension) for saving the CSV.
    - `content_code` (int): A code representing the stored content in `_content_code_map`.

- **Output**:
    `success` (bool):  
    - `True` if the data is successfully saved as a CSV.
    - `False` if the content is missing, empty, or an error occurs.

- **Behavior**:
    1. Retrieves content using `content_code` from `_content_code_map`.
    2. Checks if the content exists and is non-empty.
    3. Converts the list of dictionaries into a Pandas DataFrame.
    4. Saves the DataFrame as a CSV file in `_user_data_save_path` with the specified `save_name`.
    5. Handles exceptions and logs errors.

- **Dictionary Structure** (Each Song Contains):  
    - `'song_name'` (`str`): Name of the song.
    - `'song_id'` (`str`): Unique ID of the song.
    - `'artist_name'` (`str`): Name of the primary artist.
    - `'artist_id'` (`str`): Unique ID of the artist.
    - `'genre'` (`str`): Genre(s) associated with the artist.
    - `'album_name'` (`str`): Name of the album the song belongs to.
    - `'date_released'` (`str`): Release date of the song.
    - `'date_added'` (`str`): Date when the song was added to the playlist.
    - `'popularity'` (`int`): Popularity score of the song on Spotify.

- **Example Output:**
    ```json
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
        }
    ]

---

#### `get_artist_top_tracks(self, artist_name)`

- Description
    Fetches and displays the top tracks of a given artist using the Spotify API.

- Parameters
    - `artist_name` (str): The name of the artist.

- Return
    - `list`: A list of tuples containing track names and their popularity scores.
    - If the artist is not found, returns a message: `"No artist found with the name 'artist_name'"`.

- Behavior
    1. Searches for the artist using Spotify's search API.
    2. If the artist exists, retrieves their `artist_id`.
    3. Fetches the artist's top tracks using the `artist_top_tracks` API.
    4. Extracts the track names and popularity scores.
    5. Displays the results in a numbered list.
    6. Returns a list of `(track_name, popularity)` tuples.

- Example Output
```
Found Artist: Ed Sheeran (ID: 6eUKZXaKkcviH0Ku9w2n3V)
1. Shape of You (Popularity: 90)
2. Perfect (Popularity: 87)
3. Bad Habits (Popularity: 85)
...
```

---

#### `logout_user(self)`

- Description
    Logs out the current authenticated Spotify user by clearing authentication cache, deleting user data files, and resetting the Spotify API instance.

- Parameters
    - **None**

- Return
    - **None**

- Behavior
    1. **Clears Spotify Authentication Cache**  
        - Deletes all files in the cache directory (`SPOTIFY_CACHE_PATH`) while keeping the folder intact.
        - Displays a message if no cache is found.

    2. **Resets Spotify API Instance (`self._sp`)**  
        - Prevents further API calls after logout.

    3. **Deletes User Data Files**  
        - Removes all files inside `self._user_data_save_path` while keeping the directory intact.
        - Ensures only files are deleted, avoiding unintended folder removal.

    4. **Handles Errors Gracefully**  
        - Catches and prints any exceptions during the logout process.

---

## Usage Example

- **driver code**:
```python
from src.SpotifyAnalyzer.SpotifyAnalyzer import SpotifyAnalysis


sa = SpotifyAnalysis()

#GET TOP ARTIST SONGS---------------SUCCESS
artist = input("\nEnter Artist :")
sa.get_artist_top_tracks(artist)


# CHECK IF TOKEN IS VALID---------------SUCCESS
sa.check_token_validity()


# CHECK REAUTHENTICATION---------------SUCCESS
sa.Reauthenticate()


#CHECK USERS PLAYLISTS LIST---------------SUCCESS
sa.get_user_id()
list_of_playlists = sa.get_list_of_playlist()
print(f"\nLIST OF PLAYLISTS")
list_of_playlist_df = pd.DataFrame(list_of_playlists)
print(list_of_playlist_df)


#CHECK USERS CURRENT PLAYLISTS CONTENT---------------SUCCESS
playlist_id = input("\nEnter playlist ID: ")
playlist_name , playlist_content  = sa.get_playlist_content(playlist_id=playlist_id)
print(f"\nPLAYLIST CONTENT : {playlist_name}\n")
playlist_df = pd.DataFrame(playlist_content)
print(playlist_df)


#GET USERS LIKED SONG DETAILS---------------SUCCESS
playlist_name, liked_song_details = sa.get_liked_songs_playlist()
liked_song_df = pd.DataFrame(liked_song_details)
print("\nplaylist naem: ",playlist_name)
print(liked_song_df)


#GET USER ID FOR CURRENT USER FROM SPOTIFY---------------SUCCESS
ui,un = sa.get_user_id()
print(f"\nuser id  = {ui}\nuser_name = {un}")


#SAVING LIST OF PLAYLIST AS CSV FILE---------------SUCCESS
playlist_name,playlist_content = sa.get_list_of_playlist()
print(f"PLAYLIST NAME: {playlist_name}")
print(pd.DataFrame(playlist_content))
print("\nSaving started")
sa.save_data_as_csv(playlist_name , content_code=1)


#SAVING THE DATA FROM SPOTIFY LOCALLY INTO CSV FILES  BY GIVING A SAVE_NAME,CONTENT---------------SUCCESS
playlist_id = input("\nEnter playlist ID: ")
playlist_name , playlist_content  = sa.get_playlist_content(playlist_id=playlist_id)
print(f"\nPLAYLIST NAME : {playlist_name}\n")
playlist_df = pd.DataFrame(playlist_content)
print(playlist_df)
print("\nSaving started")
sa.save_data_as_csv(playlist_name , content_code=2)


#SAVING LIKED PLAYLIST DATA INTO CSV---------------SUCCESS
playlist_name , playlist_content  = sa.get_liked_songs_playlist()
print(f"\nPLAYLIST NAME : {playlist_name}\n")
playlist_df = pd.DataFrame(playlist_content)
print(playlist_df)
print("\nSaving started")
sa.save_data_as_csv(playlist_name , content_code=3)

#GET METRIC FOR EVERY SONG IN PLAYLIST USING ITS CONTENT_CODE_MAP---------------FAILED
playlist_id = input("\nEnter playlist ID: ")
playlist_name , playlist_content  = sa.get_playlist_content(playlist_id=playlist_id)
sa.get_track_metrics(content_code=2)

#LOG OUT THE USER AFTER SPOTIFY DATA EXTRACTION IS DONE(TO BE USED IN CORES WHEN USER EXISTS THE APPLICATION)---------------SUCCESS
sa.logout_user()
