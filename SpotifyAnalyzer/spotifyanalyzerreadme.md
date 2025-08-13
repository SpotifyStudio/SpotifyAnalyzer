# SpotifyAnalyzer.py - Complete Documentation

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Environment Setup](#environment-setup)
- [Quick Start](#quick-start)
- [API Reference](#api-reference)
- [Usage Examples](#usage-examples)
- [Data Structures](#data-structures)
- [Error Handling](#error-handling)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## 🎯 Overview

`SpotifyAnalyzer.py` is a comprehensive Python class that provides seamless integration with the Spotify Web API for analyzing user music data. It offers a complete solution for authenticating users, fetching playlists, analyzing liked songs, and managing music data with robust error handling and data persistence capabilities.

### Key Capabilities
- **OAuth2 Authentication**: Secure user authentication with automatic token management
- **Playlist Analysis**: Fetch and analyze user playlists with detailed track information
- **Liked Songs Processing**: Retrieve and process user's liked songs collection
- **Artist Information**: Get detailed artist data and top tracks
- **Data Export**: Save music data to CSV format for further analysis
- **Token Management**: Automatic token validation and refresh mechanisms

## ✨ Features

### 🔐 Authentication & Security
- OAuth2 authentication flow with Spotify
- Automatic token validation and refresh
- Secure credential management via environment variables
- Session management with cache persistence

### 📊 Data Retrieval
- User profile information (ID, display name)
- Complete playlist listings with metadata
- Detailed track information including:
  - Song metadata (name, ID, popularity)
  - Artist information (name, ID, genres)
  - Album details (name, release date)
  - Timestamps (date added, release date)
- Liked songs collection with full metadata
- Artist top tracks with popularity scores

### 💾 Data Management
- Structured content mapping system
- CSV export functionality
- Organized data storage
- Cache management for performance

### 🛠️ Utility Functions
- Token validity checking
- Reauthentication handling
- User logout with cleanup
- Error handling and logging

## 🚀 Installation

### Prerequisites
- Python 3.12.6 or higher
- Spotify Developer Account
- Required Python packages (see dependencies)

### Dependencies
```bash
pip install spotipy python-dotenv pandas
```

Or using Poetry:
```bash
poetry add spotipy python-dotenv pandas
```

### Required Packages
- `spotipy` - Spotify Web API wrapper
- `python-dotenv` - Environment variable management
- `pandas` - Data manipulation and CSV export

## 🔧 Environment Setup

### 1. Spotify Developer Setup
1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new application
3. Note your Client ID and Client Secret
4. Add redirect URI (e.g., `http://localhost:8888/callback`)

### 2. Environment Variables
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

## 🏃‍♂️ Quick Start

### Basic Usage
```python
from SpotifyAnalyzer import SpotifyAnalysis

# Initialize the analyzer
spotify = SpotifyAnalysis()

# Get user information
user_id, user_name = spotify.get_user_id()
print(f"User: {user_name} (ID: {user_id})")

# Get user's playlists
playlist_label, playlists = spotify.get_list_of_playlist()
print(f"Found {len(playlists)} playlists")

# Get playlist content
if playlists:
    playlist_id = playlists[0]['id']
    playlist_name, tracks = spotify.get_playlist_content(playlist_id)
    print(f"Playlist '{playlist_name}' has {len(tracks)} tracks")

# Get liked songs
liked_label, liked_songs = spotify.get_liked_songs_playlist()
print(f"User has {len(liked_songs)} liked songs")

# Save data to CSV
spotify.save_data_as_csv("my_playlists", 1)  # Save playlists
spotify.save_data_as_csv("my_liked_songs", 3)  # Save liked songs
```

## 📚 API Reference

### Class: `SpotifyAnalysis`

#### Constructor
```python
def __init__(self)
```
Initializes the Spotify API client and sets up authentication.

**Raises:**
- `ValueError`: If Spotify Client ID or Client Secret is not set in environment variables

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

#### Methods

##### `get_user_id()`
```python
def get_user_id(self) -> tuple[str, str] | None
```
Fetches the current authenticated user's Spotify user ID and display name.

**Returns:**
- `tuple[str, str]`: (user_id, user_name) or `None` if error occurs

##### `check_token_validity()`
```python
def check_token_validity(self) -> bool
```
Verifies the validity of the current Spotify API token.

**Returns:**
- `bool`: `True` if token is valid, `False` if invalid/expired

##### `Reauthenticate()`
```python
def Reauthenticate(self) -> None
```
Prompts user to reauthenticate and updates the Spotify API token.

##### `get_list_of_playlist(limit: int = 20)`
```python
def get_list_of_playlist(self, limit: int = 20) -> tuple[str, list[dict]]
```
Fetches the playlists of the authenticated Spotify user.

**Parameters:**
- `limit` (int): Number of playlists to fetch (default: 20)

**Returns:**
- `tuple[str, list[dict]]`: (label, playlists) where each playlist dict contains:
  - `name` (str): Playlist name
  - `id` (str): Playlist ID

##### `get_playlist_content(playlist_id: str)`
```python
def get_playlist_content(self, playlist_id: str) -> tuple[str, list[dict]]
```
Fetches the contents of a Spotify playlist using its ID.

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

##### `get_liked_songs_playlist()`
```python
def get_liked_songs_playlist(self) -> tuple[str, list[dict]]
```
Fetches the authenticated user's liked songs.

**Returns:**
- `tuple[str, list[dict]]`: (label, liked_songs) with same track structure as playlist content

##### `save_data_as_csv(save_name: str, content_code: int)`
```python
def save_data_as_csv(self, save_name: str, content_code: int) -> bool
```
Saves the specified content as a CSV file.

**Parameters:**
- `save_name` (str): Desired filename (without extension)
- `content_code` (int): Content code (1, 2, or 3)

**Returns:**
- `bool`: `True` if successful, `False` if error

##### `get_artist_top_tracks(artist_name: str)`
```python
def get_artist_top_tracks(self, artist_name: str) -> list[tuple[str, int]] | str
```
Fetches and displays the top tracks of a given artist.

**Parameters:**
- `artist_name` (str): Name of the artist

**Returns:**
- `list[tuple[str, int]]`: List of (track_name, popularity) tuples
- `str`: Error message if artist not found

##### `logout_user()`
```python
def logout_user(self) -> None
```
Logs out the current user by clearing cache and deleting user data files.

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

### Example 2: Data Analysis Pipeline
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

### Example 3: Playlist Comparison
```python
from SpotifyAnalyzer import SpotifyAnalysis

spotify = SpotifyAnalysis()

# Get playlists
label, playlists = spotify.get_list_of_playlist()

# Compare two playlists
if len(playlists) >= 2:
    playlist1_id = playlists[0]['id']
    playlist2_id = playlists[1]['id']
    
    name1, tracks1 = spotify.get_playlist_content(playlist1_id)
    name2, tracks2 = spotify.get_playlist_content(playlist2_id)
    
    print(f"Comparing '{name1}' vs '{name2}'")
    print(f"Playlist 1: {len(tracks1)} tracks")
    print(f"Playlist 2: {len(tracks2)} tracks")
    
    # Find common artists
    artists1 = set(track['artist_name'] for track in tracks1)
    artists2 = set(track['artist_name'] for track in tracks2)
    common_artists = artists1.intersection(artists2)
    
    print(f"Common artists: {len(common_artists)}")
    for artist in list(common_artists)[:5]:
        print(f"  - {artist}")
```

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

### Error Recovery Strategies

1. **Token Issues**: Use `check_token_validity()` and `Reauthenticate()`
2. **Rate Limiting**: Implement exponential backoff
3. **Network Issues**: Retry with delay
4. **Data Validation**: Check return values before processing

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

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Spotify Web API for providing the music data
- Spotipy library for Python Spotify API integration
- Pandas for data manipulation capabilities

---

**Note**: This documentation covers the complete functionality of `SpotifyAnalyzer.py`. For additional features like genre prediction, see the `GenrePrediction.py` documentation. 