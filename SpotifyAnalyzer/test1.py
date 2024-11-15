import sys
import os

# Dynamically add the src directory to the module search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Import after modifying the path
#from SpotifyAnalyzer.utils import GenrePrediction
from src.SpotifyAnalyzer.utils import GenrePrediction

# Example usage
audio_path = "tests/metal_demo.mp3"
mod = GenrePrediction()
output = mod.predict_genre_chain(audio_path)
print(output)
