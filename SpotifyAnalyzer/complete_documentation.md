# SpotifyAnalyzer - Complete Documentation

## �� Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [Core Components](#core-components)
  - [SpotifyAnalysis Class](#spotifyanalysis-class)
  - [GenrePrediction Class](#genreprediction-class)
- [API Reference](#api-reference)
- [Usage Examples](#usage-examples)
- [Data Structures](#data-structures)
- [Error Handling](#error-handling)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

---

## 🎯 Overview

The SpotifyAnalyzer project is a comprehensive Python package that provides seamless integration with the Spotify Web API for analyzing user music data. It consists of two main components:

1. **SpotifyAnalysis** - Handles Spotify API authentication, playlist retrieval, and data management
2. **GenrePrediction** - Provides machine learning-based genre classification for audio files

### Key Capabilities

- **OAuth2 Authentication**: Secure user authentication with automatic token management
- **Playlist Analysis**: Fetch and analyze user playlists with detailed track information
- **Liked Songs Processing**: Retrieve and process user's liked songs collection
- **Artist Information**: Get detailed artist data and top tracks
- **Data Export**: Save music data to CSV format for further analysis
- **Genre Prediction**: ML-based audio genre classification using RNN and melspectrograms
- **Token Management**: Automatic token validation and refresh mechanisms

---

## 📁 Project Structure

```
SpotifyAnalyzer/
├── src/
│   ├── SpotifyAnalyzer/
│   │   ├── __init__.py
│   │   ├── core.py
│   │   ├── GenrePrediction.py
│   │   └── SpotifyAnalyzer.py
│   ├── audio_stored/
│   ├── Models/
│   ├── spotify_cache/
│   └── user_data_save/
├── tests/
├── requirements.txt
├── pyproject.toml
└── setup.py
```

---

## 🚀 Installation & Setup

### Prerequisites

- Python 3.12.6 or higher
- Spotify Developer Account
- Required Python packages (see dependencies)

### Dependencies

```bash
pip install spotipy python-dotenv pandas tensorflow librosa numpy
```

Or using Poetry:

```bash
poetry add spotipy python-dotenv pandas tensorflow librosa numpy
```

### Required Packages

- `spotipy` - Spotify Web API wrapper
- `python-dotenv` - Environment variable management
- `pandas` - Data manipulation and CSV export
- `tensorflow` - Machine learning framework for genre prediction
- `librosa` - Audio processing library
- `numpy` - Numerical computing

### Environment Setup

#### 1. Spotify Developer Setup

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new application
3. Note your Client ID and Client Secret
4. Add redirect URI (e.g., `http://localhost:8888/callback`)

#### 2. Environment Variables

Create `.env.api` file:

```env
SPOTIFY_CLIENT_ID=your_client_id_here
SPOTIFY_CLIENT_SECRET=your_client_secret_here
SPOTIFY_REDIRECT_URI=http://localhost:8888/callback
```

Create `.env.path` file:

```env
SPOTIFY_CACHE_PATH=./spotify_cache
USER_DATA_SAVE=./user_data_save
```

---

## 🔧 Core Components

### SpotifyAnalysis Class

The `SpotifyAnalysis` class is responsible for analyzing a user's Spotify account by retrieving and managing playlist and song data using the Spotify API. It handles authentication, playlist retrieval, token management, and data organization in a structured manner.

**Features:**

- Authenticate users via Spotify OAuth
- Retrieve user ID and display name
- Validate and refresh authentication tokens
- Fetch playlists and their details
- Retrieve song information from playlists
- Maintain a structured mapping of fetched content

**Instance Variables:**

- `_spotify_client_id` (str): Spotify API Client ID
- `_spotify_client_secret` (str): Spotify API Client Secret
- `_spotify_redirect_uri` (str): OAuth redirect URI
- `_scope` (str): Required permissions
- `_user_data_save_path` (str): Path for saving user data
- `_sp` (Spotify): Authenticated Spotify API client
- `_user_id` (str): User's Spotify ID
- `_user_name` (str): User's display name
- `_Playlists_Details` (list): User's playlists
- `_current_playlist_content` (list): Current playlist tracks
- `_liked_playlist_content` (list): User's liked songs

**Content Code Mapping:**

- `1` → Playlists details
- `2` → Current playlist content
- `3` → Liked songs content

### GenrePrediction Class

The `GenrePrediction` class is responsible for predicting the genre of a given audio file. It handles tasks such as converting MP3 files to WAV, preprocessing audio files into Mel-spectrograms, and using a pre-trained machine learning model to classify the genre.

**Features:**

- Convert MP3 files to WAV format
- Preprocess audio into melspectrograms
- Load and use pre-trained ML models
- Predict genres using RNN architecture
- Handle various audio file formats

---

## 📚 API Reference

### SpotifyAnalysis Methods

#### `__init__(self)`

Initializes the `SpotifyAnalysis` class by setting up authentication with the Spotify API.

**Raises:**

- `ValueError`: If Spotify Client ID or Client Secret is not set in environment variables

**Instance Variables:**

- `self._spotify_client_id` (str): Spotify API Client ID loaded from environment variables
- `self._spotify_client_secret` (str): Spotify API Client Secret loaded from environment variables
- `self._spotify_redirect_uri` (str): Redirect URI for OAuth authentication
- `self._scope` (str): Required permissions for accessing Spotify data
- `self._user_data_save_path` (str): Path to save user data
- `self._sp` (Spotify): Authenticated Spotify API client instance
- `self._user_id` (str): Stores the user's unique Spotify ID
- `self._user_name` (str): Stores the user's Spotify display name
- `self._Playlists_Details` (list): Stores details of the user's playlists
- `self._current_playlist_content` (list): Stores tracks of the currently selected playlist
- `self._liked_playlist_content` (list): Stores tracks from the user's liked songs

#### `get_user_id(self) -> tuple[str, str] | None`

Retrieves the currently authenticated user's Spotify user ID and display name.

**Returns:**

- `tuple[str, str]`: (user_id, user_name) or `None` if error occurs

#### `check_token_validity(self) -> bool`

Verifies whether the current Spotify API token is valid. If the token is expired or invalid, it triggers reauthentication.

**Returns:**

- `bool`: `True` if token is valid, `False` if token is expired or invalid

#### `Reauthenticate(self) -> None`

Prompts the user to reauthenticate with Spotify and updates the API token.

**Behavior:**

- Re-initiates authentication using `SpotifyOAuth`
- Updates the authentication manager with a new token
- Replaces the existing Spotify API client instance with the newly authenticated session
- Prints `"Authentication successful. Token updated."` upon success

#### `get_list_of_playlist(limit: int = 20) -> tuple[str, list[dict]]`

Fetches and returns the playlists of the authenticated Spotify user.

**Parameters:**

- `limit` (int): Number of playlists to fetch per request (default: 20)

**Returns:**

- `tuple[str, list[dict]]`: (label, playlists) where each playlist dict contains:
  - `name` (str): Playlist name
  - `id` (str): Playlist ID

**Example Output:**

```json
[
  { "name": "My Favorite Songs", "id": "3FvDkjskH5l" },
  { "name": "Chill Vibes", "id": "8hHdYtB24zA" },
  { "name": "Workout Hits", "id": "9KlsM3rA76P" }
]
```

#### `get_playlist_content(playlist_id: str) -> tuple[str, list[dict]]`

Fetches the contents of a Spotify playlist using its playlist ID. Returns details such as song name, artist name, genre, album name, release date, and popularity.

**Parameters:**

- `playlist_id` (str): Unique Spotify playlist ID

**Returns:**

- `tuple[str, list[dict]]`: (playlist_name, tracks) where each track dict contains:
  - `song_name` (str): Track name
  - `song_id` (str): Track ID
  - `artist_name` (str): Primary artist name
  - `artist_id` (str): Artist ID
  - `genre` (str): Artist genres
  - `album_name` (str): Album name
  - `date_released` (str): Release date
  - `date_added` (str): Date added to playlist
  - `popularity` (int): Spotify popularity score

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
```

#### `get_liked_songs_playlist() -> tuple[str, list[dict]]`

Fetches the contents of a Spotify Liked songs playlist. Returns details such as song name, artist name, genre, album name, release date, and popularity.

**Returns:**

- `tuple[str, list[dict]]`: (label, liked_songs) with same track structure as playlist content

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
```

#### `save_data_as_csv(save_name: str, content_code: int) -> bool`

Saves the specified content as a CSV file.

**Parameters:**

- `save_name` (str): Desired filename (without extension)
- `content_code` (int): Content code (1, 2, or 3)

**Returns:**

- `bool`: `True` if successful, `False` if error

**Behavior:**

1. Retrieves content using `content_code` from `_content_code_map`
2. Checks if the content exists and is non-empty
3. Converts the list of dictionaries into a Pandas DataFrame
4. Saves the DataFrame as a CSV file in `_user_data_save_path` with the specified `save_name`
5. Handles exceptions and logs errors

#### `get_artist_top_tracks(artist_name: str) -> list[tuple[str, int]] | str`

Fetches and displays the top tracks of a given artist using the Spotify API.

**Parameters:**

- `artist_name` (str): Name of the artist

**Returns:**

- `list[tuple[str, int]]`: List of (track_name, popularity) tuples
- `str`: Error message if artist not found

**Behavior:**

1. Searches for the artist using Spotify's search API
2. If the artist exists, retrieves their `artist_id`
3. Fetches the artist's top tracks using the `artist_top_tracks` API
4. Extracts the track names and popularity scores
5. Displays the results in a numbered list
6. Returns a list of `(track_name, popularity)` tuples

**Example Output:**

```
Found Artist: Ed Sheeran (ID: 6eUKZXaKkcviH0Ku9w2n3V)
1. Shape of You (Popularity: 90)
2. Perfect (Popularity: 87)
3. Bad Habits (Popularity: 85)
...
```

#### `logout_user() -> None`

Logs out the current authenticated Spotify user by clearing authentication cache, deleting user data files, and resetting the Spotify API instance.

**Behavior:**

1. **Clears Spotify Authentication Cache**

   - Deletes all files in the cache directory (`SPOTIFY_CACHE_PATH`) while keeping the folder intact
   - Displays a message if no cache is found

2. **Resets Spotify API Instance (`self._sp`)**

   - Prevents further API calls after logout

3. **Deletes User Data Files**

   - Removes all files inside `self._user_data_save_path` while keeping the directory intact
   - Ensures only files are deleted, avoiding unintended folder removal

4. **Handles Errors Gracefully**
   - Catches and prints any exceptions during the logout process

### GenrePrediction Methods

#### `__init__(self)`

Initializes the `GenrePrediction` class, setting up paths for the audio directory and the model. It also attempts to load the pre-trained machine learning model.

**Instance Variables:**

- A list of genres
- Paths to the audio directory and model
- Attempts to load the model using the `load_genre_model()` method

#### `get_current_audio_name(self) -> str`

Returns the name of the next audio file to be saved. This is based on the existing files in the audio directory, ensuring unique filenames by incrementing the number in the filename.

**Returns:**

- `str`: The name of the next audio file (e.g., 'audio_1.wav', 'audio_2.wav')

#### `copy_wav_to_folder(self, audio_path: str) -> None`

Copies a given WAV file to the target folder and renames it using the current naming convention for audio files.

**Parameters:**

- `audio_path` (str): The path to the audio file to be copied

#### `mp3_to_wav(self, input_audio_path: str) -> None`

Converts an MP3 file to WAV format using `ffmpeg` and stores it in the specified audio directory.

**Parameters:**

- `input_audio_path` (str): Path to the MP3 file to be converted

#### `load_genre_model(self) -> model | None`

Loads the pre-trained machine learning model for genre prediction from the specified model path.

**Returns:**

- `model`: A loaded Keras model for genre prediction
- `None`: If there is an error loading the model

#### `preprocess_audio(self, target_shape: tuple = (150, 150)) -> np.ndarray | None`

Preprocesses the audio file by splitting it into chunks, generating Mel-spectrograms for each chunk, and resizing them to match the target shape for the model input.

**Parameters:**

- `target_shape` (tuple): The desired output shape for the Mel-spectrogram (default: (150, 150))

**Returns:**

- `np.ndarray`: A 3D numpy array containing the preprocessed Mel-spectrogram chunks
- `None`: If an error occurs during preprocessing or loading the audio

#### `prediction(self, processed_audio: np.ndarray) -> int`

Predicts the genre of the audio based on the processed Mel-spectrograms. The model is used to classify the genre, and the genre with the highest predicted score is selected.

**Parameters:**

- `processed_audio` (np.ndarray): The preprocessed Mel-spectrogram chunks to be passed to the model

**Returns:**

- `int`: The index of the predicted genre in the `self._genres` list

#### `predict_genre_chain(self, audio_path: str, target_shape: tuple = (150, 150)) -> str | None`

The full pipeline for predicting the genre of an audio file. It handles the file format check (MP3 or WAV), converts MP3 to WAV if needed, preprocesses the audio, and uses the model to predict the genre.

**Parameters:**

- `audio_path` (str): Path to the audio file to be predicted (either MP3 or WAV)
- `target_shape` (tuple): The desired shape for resizing the Mel-spectrogram (default: (150, 150))

**Returns:**

- `str`: The predicted genre label (e.g., 'rock', 'pop')
- `None`: If there was an error in the process (e.g., unsupported file format or preprocessing failure)

---

## 💡 Usage Examples

### Example 1: Complete User Analysis

```python
from SpotifyAnalyzer import SpotifyAnalysis

# Initialize
spotify = SpotifyAnalysis()

# Check authentication
if not spotify.check_token_validity():
    print("Authentication required")
    exit()

# Get user info
user_id, user_name = spotify.get_user_id()
print(f"Analyzing music for: {user_name}")

# Get all playlists
label, playlists = spotify.get_list_of_playlist(limit=50)
print(f"Found {len(playlists)} playlists")

# Analyze each playlist
for playlist in playlists:
    name, tracks = spotify.get_playlist_content(playlist['id'])
    print(f"Playlist '{name}': {len(tracks)} tracks")

    # Save playlist data
    spotify.save_data_as_csv(f"playlist_{name}", 2)

# Get liked songs
label, liked_songs = spotify.get_liked_songs_playlist()
print(f"Liked songs: {len(liked_songs)} tracks")
spotify.save_data_as_csv("liked_songs", 3)

# Get artist top tracks
artist_tracks = spotify.get_artist_top_tracks("The Weeknd")
print("Top tracks by The Weeknd:")
for track, popularity in artist_tracks:
    print(f"  {track} (Popularity: {popularity})")

# Cleanup
spotify.logout_user()
```

### Example 2: Genre Prediction

```python
import sys
import os

# Dynamically add the src directory to the module search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Import after modifying the path
from src.SpotifyAnalyzer.utils import GenrePrediction

# Initialize genre prediction
mod = GenrePrediction()

# Predict genre for an audio file
audio_path = "tests/metal_demo.mp3"
predicted_genre = mod.predict_genre_chain(audio_path)
print(f"Predicted genre: {predicted_genre}")
```

### Example 3: Data Analysis Pipeline

```python
import pandas as pd
from SpotifyAnalyzer import SpotifyAnalysis

# Setup
spotify = SpotifyAnalysis()

# Fetch data
user_id, user_name = spotify.get_user_id()
label, playlists = spotify.get_list_of_playlist()
label, liked_songs = spotify.get_liked_songs_playlist()

# Convert to DataFrames for analysis
playlists_df = pd.DataFrame(playlists)
liked_df = pd.DataFrame(liked_songs)

# Analyze music preferences
print("=== Music Analysis ===")
print(f"Total playlists: {len(playlists)}")
print(f"Total liked songs: {len(liked_songs)}")

# Genre analysis
if not liked_df.empty:
    genre_counts = liked_df['genre'].value_counts()
    print("\nTop genres in liked songs:")
    print(genre_counts.head(10))

# Popularity analysis
if not liked_df.empty:
    avg_popularity = liked_df['popularity'].mean()
    print(f"\nAverage song popularity: {avg_popularity:.1f}")

# Save comprehensive report
spotify.save_data_as_csv("music_analysis_report", 3)
```

### Example 4: Complete Driver Code

```python
from src.SpotifyAnalyzer.SpotifyAnalyzer import SpotifyAnalysis
import pandas as pd

# Initialize
sa = SpotifyAnalysis()

# Get user information
user_id, user_name = sa.get_user_id()
print(f"User: {user_name} (ID: {user_id})")

# Get playlists
label, playlists = sa.get_list_of_playlist()
print(f"Found {len(playlists)} playlists")
playlist_df = pd.DataFrame(playlists)
print(playlist_df)

# Get playlist content
playlist_id = input("\nEnter playlist ID: ")
playlist_name, playlist_content = sa.get_playlist_content(playlist_id)
print(f"\nPLAYLIST CONTENT: {playlist_name}")
playlist_df = pd.DataFrame(playlist_content)
print(playlist_df)

# Get liked songs
playlist_name, liked_song_details = sa.get_liked_songs_playlist()
liked_song_df = pd.DataFrame(liked_song_details)
print(f"\nLiked Songs: {playlist_name}")
print(liked_song_df)

# Save data to CSV
sa.save_data_as_csv("my_playlists", 1)  # Save playlists
sa.save_data_as_csv("my_liked_songs", 3)  # Save liked songs

# Get artist top tracks
artist = input("\nEnter Artist: ")
sa.get_artist_top_tracks(artist)

# Logout
sa.logout_user()
```

### Example 5: Advanced Usage with Both Components

```python
from src.SpotifyAnalyzer.SpotifyAnalyzer import SpotifyAnalysis
from src.SpotifyAnalyzer.utils import GenrePrediction
import pandas as pd

# Initialize both components
spotify = SpotifyAnalysis()
genre_predictor = GenrePrediction()

# Get user's liked songs
label, liked_songs = spotify.get_liked_songs_playlist()
print(f"Analyzing {len(liked_songs)} liked songs")

# Analyze genres from Spotify data
liked_df = pd.DataFrame(liked_songs)
if not liked_df.empty:
    spotify_genres = liked_df['genre'].value_counts()
    print("\nTop genres from Spotify data:")
    print(spotify_genres.head(5))

# Example: Predict genre for a local audio file
audio_file = "path/to/local/audio.mp3"
try:
    predicted_genre = genre_predictor.predict_genre_chain(audio_file)
    print(f"\nPredicted genre for {audio_file}: {predicted_genre}")
except Exception as e:
    print(f"Genre prediction failed: {e}")

# Save comprehensive analysis
spotify.save_data_as_csv("complete_analysis", 3)
```

---

## 📊 Data Structures

### Playlist Object

```python
{
    "name": "My Playlist",
    "id": "37i9dQZF1DXcBWIGoYBM5M"
}
```

### Track Object

```python
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
}
```

### Liked Song Object

```python
{
    "song_name": "Shape of You",
    "song_url": "7qiZfU4dY1lWllzX7mPBI3",  # Note: this is actually the song_id
    "artist_name": "Ed Sheeran",
    "artist_id": "6eUKZXaKkcviH0Ku9w2n3V",
    "genre": "Pop",
    "album_name": "Divide",
    "date_released": "2017-01-06",
    "date_added": "2023-07-16T08:20:30Z",
    "popularity": 95
}
```

---

## ⚠️ Error Handling

### Common Exceptions

#### Authentication Errors

```python
try:
    spotify = SpotifyAnalysis()
except ValueError as e:
    print(f"Authentication setup failed: {e}")
    # Check environment variables
```

#### API Rate Limiting

```python
try:
    playlists = spotify.get_list_of_playlist()
except Exception as e:
    if "rate limit" in str(e).lower():
        print("Rate limit exceeded. Please wait before retrying.")
    else:
        print(f"API error: {e}")
```

#### Token Expiration

```python
if not spotify.check_token_validity():
    print("Token expired. Reauthenticating...")
    spotify.Reauthenticate()
```

#### Genre Prediction Errors

```python
try:
    predicted_genre = mod.predict_genre_chain(audio_path)
    if predicted_genre is None:
        print("Failed to predict genre. Check audio file format.")
except Exception as e:
    print(f"Genre prediction error: {e}")
```

### Error Recovery Strategies

1. **Token Issues**: Use `check_token_validity()` and `Reauthenticate()`
2. **Rate Limiting**: Implement exponential backoff
3. **Network Issues**: Retry with delay
4. **Data Validation**: Check return values before processing
5. **Audio Format Issues**: Ensure supported formats (MP3, WAV)

---

## 🔧 Troubleshooting

### Common Issues

#### 1. Authentication Problems

**Problem**: `ValueError: Spotify client ID and secret must be set`
**Solution**:

- Verify `.env.api` file exists and contains correct credentials
- Check Spotify Developer Dashboard for correct Client ID/Secret
- Ensure redirect URI matches exactly

#### 2. Empty Playlist Results

**Problem**: API returns empty playlist list
**Solution**:

- Check if user has public playlists
- Verify API permissions include `playlist-read-private`
- Check for rate limiting

#### 3. Token Expiration

**Problem**: API calls fail with authentication errors
**Solution**:

```python
if not spotify.check_token_validity():
    spotify.Reauthenticate()
```

#### 4. File Permission Errors

**Problem**: Cannot save CSV files
**Solution**:

- Check write permissions for `USER_DATA_SAVE` directory
- Ensure directory exists and is writable

#### 5. Genre Prediction Issues

**Problem**: Genre prediction fails or returns None
**Solution**:

- Ensure audio file is in supported format (MP3 or WAV)
- Check if model file exists in Models directory
- Verify audio file is not corrupted
- Check if ffmpeg is installed for MP3 conversion

### Debug Mode

Enable detailed logging for troubleshooting:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### API Limits

- **Rate Limits**: 100 requests per 100 seconds per user
- **Playlist Limits**: 100 tracks per request (handled automatically)
- **Liked Songs**: 50 tracks per request (handled automatically)

---

## 🤝 Contributing

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Install development dependencies
4. Make changes with proper testing
5. Submit a pull request

### Code Style

- Follow PEP 8 guidelines
- Add comprehensive docstrings
- Include type hints
- Write unit tests for new features

### Testing

```bash
# Run tests
python -m pytest tests/

# Run with coverage
python -m pytest --cov=SpotifyAnalyzer tests/
```

### Testing Genre Prediction

```python
# Test genre prediction
audio_path = "tests/metal_demo.mp3"
mod = GenrePrediction()
output = mod.predict_genre_chain(audio_path)
print(output)
```

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Spotify Web API for providing the music data
- Spotipy library for Python Spotify API integration
- Pandas for data manipulation capabilities
- TensorFlow for machine learning framework
- Librosa for audio processing capabilities

---

**Note**: This documentation covers the complete functionality of the SpotifyAnalyzer project, including both the SpotifyAnalysis and GenrePrediction components. For specific implementation details, refer to the individual class documentation sections.
