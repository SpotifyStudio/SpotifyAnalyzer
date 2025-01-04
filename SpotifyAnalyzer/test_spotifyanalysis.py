import sys
import os

# Dynamically add the src directory to the module search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Import after modifying the path
#from SpotifyAnalyzer.utils import GenrePrediction
from src.SpotifyAnalyzer.SpotifyAnalyzer import SpotifyAnalysis

sa = SpotifyAnalysis()

#GET TOP ARTIST SONGS
# artist = input("\nEnter Artist :")
# sa.get_artist_top_tracks(artist)


# CHECK IF TOKEN IS VALID
# sa.check_token_validity()

# CHECK REAUTHENTICATION
sa.Reauthenticate()




