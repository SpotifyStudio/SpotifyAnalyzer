import sys
import os

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

#CHECK USERS LIKED SONGS---------------FAILED
# liked_songs = sa.get_liked_songs()
# print("Liked Songs:")
# for i, song in enumerate(liked_songs, 1):
#     print(f"{i}. {song}")

#CHECK USERS PLAYLISTS---------------SUCCESS
# list_of_playlists = sa.get_list_of_playlist()
# print(f"\nFIELD\tVALUE")
# for playlist in list_of_playlists:
#     print(f"\nName: {playlist['name']} \t ID: {playlist['id']}")