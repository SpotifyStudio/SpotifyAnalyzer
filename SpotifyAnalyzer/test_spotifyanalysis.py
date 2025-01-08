import sys
import os
import pandas as pd

# Dynamically add the src directory to the module search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Import after modifying the path
#from SpotifyAnalyzer.utils import GenrePrediction
from src.SpotifyAnalyzer.SpotifyAnalyzer import SpotifyAnalysis

sa = SpotifyAnalysis()

#GET TOP ARTIST SONGS---------------SUCCESS
# artist = input("\nEnter Artist :")
# sa.get_artist_top_tracks(artist)


# CHECK IF TOKEN IS VALID---------------SUCCESS
# sa.check_token_validity()


# CHECK REAUTHENTICATION---------------SUCCESS
# sa.Reauthenticate()


#CHECK USERS PLAYLISTS LIST---------------SUCCESS
# list_of_playlists = sa.get_list_of_playlist()
# print(f"\nLIST OF PLAYLISTS")
# list_of_playlist_df = pd.DataFrame(list_of_playlists)
# print(list_of_playlist_df)


#CHECK USERS CURRENT PLAYLISTS CONTENT---------------SUCCESS
# playlist_id = input("\nEnter playlist ID: ")
# playlist_content = sa.get_playlist_content(playlist_id=playlist_id)
# print(f"\nPLAYLIST CONTENT\n")
# playlist_df = pd.DataFrame(playlist_content)
# print(playlist_df)


#GET USERS LIKED SONG DETAILS---------------FAILED
liked_song_details = sa.get_liked_songs_playlist()
liked_song_df = pd.DataFrame(liked_song_details)
print("\nLIKED SONGS")
print(liked_song_df)