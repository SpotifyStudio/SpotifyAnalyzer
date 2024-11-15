# SpotifyAnalyzer - utils.py Documentation

## Overview

The `utils.py` file in the SpotifyAnalyzer project provides utility functions and classes that facilitate the processing of Spotify data. These utilities are used for various tasks such as data manipulation, transformation, and other helper functionalities essential for the main analysis.

---

## Table of Contents

- [Classes](#classes)
  - [GenrePrediction](#genreprediction)
- [Functions](#functions)
  - [**init**(self)](#initself)
  - [get_current_audio_name(self)](#get_current_audio_name)
  - [copy_wav_to_folder(self, audio_path)](#copy_wav_to_folderself-audio_path)
  - [mp3_to_wav(self, input_audio_path)](#mp3_to_wavself-input_audio_path)
  - [load_genre_model(self)](#load_genre_modelself)
  - [preprocess_audio(self, target_shape=(150, 150))](#preprocess_audioself-target_shape150-150)
  - [prediction(self, processed_audio)](#predictionself-processed_audio)
  - [predict_genre_chain(self, audio_path, target_shape=(150, 150))](#predict_genre_chainself-audio_path-target_shape150-150)
- [Usage Example](#usage-example)

---

## Classes

### GenrePrediction

**Description**:  
The `GenrePrediction` class is responsible for predicting the genre of a given audio file. It handles tasks such as converting MP3 files to WAV, preprocessing audio files into Mel-spectrograms, and using a pre-trained machine learning model to classify the genre.

---

### Methods

---

#### `__init__(self)`

- **Description**:  
  Initializes the `GenrePrediction` class, setting up paths for the audio directory and the model. It also attempts to load the pre-trained machine learning model.

- **Input**:

  - None

- **Output**:  
  Initializes the `GenrePrediction` object with:
  - A list of genres.
  - Paths to the audio directory and model.
  - Attempts to load the model using the `load_genre_model()` method.

---

#### `get_current_audio_name(self)`

- **Description**:  
  Returns the name of the next audio file to be saved. This is based on the existing files in the audio directory, ensuring unique filenames by incrementing the number in the filename.

- **Input**:

  - None

- **Output**:
  - `str`: The name of the next audio file (e.g., 'audio_1.wav', 'audio_2.wav').

---

#### `copy_wav_to_folder(self, audio_path)`

- **Description**:  
  Copies a given WAV file to the target folder and renames it using the current naming convention for audio files.

- **Input**:

  - `audio_path` (`str`): The path to the audio file to be copied.

- **Output**:
  - None

---

#### `mp3_to_wav(self, input_audio_path)`

- **Description**:  
  Converts an MP3 file to WAV format using `ffmpeg` and stores it in the specified audio directory.

- **Input**:

  - `input_audio_path` (`str`): Path to the MP3 file to be converted.

- **Output**:
  - None

---

#### `load_genre_model(self)`

- **Description**:  
  Loads the pre-trained machine learning model for genre prediction from the specified model path.

- **Input**:

  - None

- **Output**:
  - `model`: A loaded Keras model for genre prediction.
  - `None`: If there is an error loading the model.

---

### `preprocess_audio(self, target_shape=(150, 150))`

- **Description**:  
  Preprocesses the audio file by splitting it into chunks, generating Mel-spectrograms for each chunk, and resizing them to match the target shape for the model input.

- **Input**:

  - `target_shape` (`tuple`): The desired output shape for the Mel-spectrogram (default is `(150, 150)`).

- **Output**:
  - `np.ndarray`: A 3D numpy array containing the preprocessed Mel-spectrogram chunks.
  - `None`: If an error occurs during preprocessing or loading the audio.

---

#### `prediction(self, processed_audio)`

- **Description**:  
  Predicts the genre of the audio based on the processed Mel-spectrograms. The model is used to classify the genre, and the genre with the highest predicted score is selected.

- **Input**:

  - `processed_audio` (`np.ndarray`): The preprocessed Mel-spectrogram chunks to be passed to the model.

- **Output**:
  - `int`: The index of the predicted genre in the `self._genres` list.

---

#### `predict_genre_chain(self, audio_path, target_shape=(150, 150))`

- **Description**:  
  The full pipeline for predicting the genre of an audio file. It handles the file format check (MP3 or WAV), converts MP3 to WAV if needed, preprocesses the audio, and uses the model to predict the genre.

- **Input**:

  - `audio_path` (`str`): Path to the audio file to be predicted (either MP3 or WAV).
  - `target_shape` (`tuple`): The desired shape for resizing the Mel-spectrogram (default is `(150, 150)`).

- **Output**:
  - `str`: The predicted genre label (e.g., 'rock', 'pop').
  - `None`: If there was an error in the process (e.g., unsupported file format or preprocessing failure).

---

---

## Usage Example

```python
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

```
