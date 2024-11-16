import sys
import os

# Dynamically add the src directory to the module search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Import after modifying the path
#from SpotifyAnalyzer.utils import GenrePrediction
from src.SpotifyAnalyzer.SpotifyAnalyzer import SpotifyAnalysis

sa = SpotifyAnalysis()

#sa.Check_spotify_api_limit()

artist = input("Enter artist name: ")
top_song_list = sa.get_top_songs_of_artist(artist)
print(f"\t{artist}\nSr no.\tSong\tpopularity")
for element in top_song_list:
    print(f"{element[0]}\t{element[1]}\t{element[2]}")

