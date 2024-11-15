import os
import subprocess
import shutil
import numpy as np
import librosa
import logging
from tensorflow.keras.models import load_model
from tensorflow.image import resize
from dotenv import load_dotenv

#load environment variables
load_dotenv(dotenv_path= ".env.path" , override=True)
load_dotenv(dotenv_path= ".env.api" , override=True)

class GenrePrediction:
    """
    A class for predicting the genre of a given audio file. The class includes methods 
    for converting MP3 files to WAV, preprocessing the audio, and using a machine learning 
    model to predict the genre of the audio.
    """
    def __init__(self):
        """
        Initializes the GenrePrediction class.

        Sets up default values for:
            - _genres: List of possible genre labels (10 genres).
            - _audio_dir_path: Path to the directory where audio files are stored.
            - _audio_path: The path to the currently processed audio file.
            - _model_path: Path to the saved machine learning model for genre prediction.
        """
        # One-hot encoding for genres
        self._genres = ('blues', 'classical', 'country', 'disco', 'hiphop', 'jazz', 'metal', 'pop', 'reggae', 'rock')
        self._audio_dir_path = os.getenv("AUDIO_DIR_PATH")
        self._audio_path = ""
        self._model_path = os.getenv("MODEL_PATH")
        # Load the model
        self._model = self.load_genre_model()
        if self._model is None:
            logging.error("Model loading failed.")
            #print(f"Model: {self._model_path} \nModel could not be loaded")
            return None
    
    def get_current_audio_name(self):
        """
        Returns the name of the next audio file to be saved, ensuring unique names based on existing files.

        Checks the directory for the most recently added file, and increments the number in its filename.

        Returns:
            str: The name of the next audio file (e.g., 'audio_1.wav', 'audio_2.wav').
        """
        try:
            files = [f for f in os.listdir(self._audio_dir_path) if os.path.isfile(os.path.join(self._audio_dir_path, f))]
            # If no files are present, return the first filename
            if not files:
                return "audio_1.wav"
            # Sort files by creation time (most recent last)
            files.sort(key=lambda f: os.path.getctime(os.path.join(self._audio_dir_path, f)))
            # Get the most recent file's name
            latest_file = files[-1]
            # Extract the base name and number from the latest file
            if latest_file.startswith("audio_") and latest_file.endswith(".wav"):
                try:
                    number = int(latest_file.split("_")[1].split(".")[0])  # Extract the number
                    return f"audio_{number + 1}.wav"  # Increment the number
                except ValueError:
                    pass
            # If no pattern matches, return a default name
            return "audio_1.wav"
        except Exception as e:
            logging.error(f"Error fetching audio name: {e}")
            return "audio_1.wav"
    
    def copy_wav_to_folder(self, audio_path):
        """
        Copies a WAV audio file to the target folder and renames it using the current audio naming convention.

        Args:
            audio_path (str): The path to the audio file to be copied.
        """
        filename = self.get_current_audio_name()
        self._audio_path = os.path.join(self._audio_dir_path, filename)
        try:
            shutil.copy(audio_path, self._audio_path)
        except Exception as e:
            logging.error(f"Failed to copy audio file: {e}")
    
    def mp3_to_wav(self, input_audio_path):
        """
        Converts an MP3 file to WAV format using ffmpeg and stores it in the target directory.

        Args:
            input_audio_path (str): Path to the MP3 audio file to be converted.

        Returns:
            None
        """
        # Make sure audio_stored exists
        os.makedirs(self._audio_dir_path, exist_ok=True)
        # Get dynamic name of current audio path
        filename = self.get_current_audio_name()
        # Create full output path
        self._audio_path = os.path.join(self._audio_dir_path, filename)
        # Convert MP3 to WAV using ffmpeg
        try:
            subprocess.run(['ffmpeg', '-i', input_audio_path, self._audio_path], check=True)
        except subprocess.CalledProcessError as e:
            logging.error(f"Error during MP3 to WAV conversion: {e}")
    
    def load_genre_model(self):
        """
        Loads the pre-trained machine learning model for genre prediction.

        Returns:
            model: A TensorFlow/Keras model used for genre prediction.
            None: If there is an error loading the model.
        """
        try:
            self.genre_model = load_model(self._model_path)
            return self.genre_model
        except Exception as e:
            logging.error(f"Error loading model: {e}")
            print(f"Error loading model: {e}")
            return None
    
    def preprocess_audio(self, target_shape=(150, 150)):
        """
        Preprocesses the audio file to generate Mel-spectrograms that are used for genre classification.

        The audio is split into chunks, and Mel-spectrograms are generated for each chunk. These are then resized
        to match the required input shape for the model.

        Args:
            target_shape (tuple): The target shape for resizing the Mel-spectrogram (default is (150, 150)).

        Returns:
            np.ndarray: A 3D numpy array containing the preprocessed Mel-spectrogram chunks (shape: (num_chunks, height, width, 1)).
            None: If the audio file cannot be loaded or an error occurs during preprocessing.
        """
        # Load audio using librosa
        try:
            audio_data, sample_rate = librosa.load(self._audio_path, sr=None)
        except Exception as e:
            logging.error(f'Failed to load audio: {self._audio_path}, Error: {e}')
            return None
        # Defining chunk and overlap duration
        chunk_duration = 4  # in seconds
        overlap_duration = 2  # in seconds
        # Convert duration to samples
        chunk_samples = chunk_duration * sample_rate
        overlap_samples = overlap_duration * sample_rate
        # Find number of total chunks
        num_chunks = int(np.ceil((len(audio_data) - chunk_samples) / (chunk_samples - overlap_samples)))
        processed_chunks = []
        # Iterate over all chunks to create Mel-spectrograms
        for i in range(num_chunks):
            # Finding start and end timestamp of chunk
            start = i * (chunk_samples - overlap_samples)
            end = start + chunk_samples
            # Extract chunk from audio_data
            chunk = audio_data[start:end]
            # Extract Mel-spectrogram for chunk
            mel_spectrogram = librosa.feature.melspectrogram(y=chunk, sr=sample_rate)
            # Resize mel_spectrogram to target shape
            mel_spectrogram = np.expand_dims(mel_spectrogram, axis=-1)
            mel_spectrogram = resize(mel_spectrogram, target_shape).numpy()
            # Add mel_spectrogram to processed_chunks list
            processed_chunks.append(mel_spectrogram)
        return np.array(processed_chunks)
    
    def prediction(self, processed_audio):
        """
        Predicts the genre of the audio based on the processed Mel-spectrograms.

        The model is used to make predictions on the preprocessed audio, and the genre with the highest
        prediction score is selected as the output.

        Args:
            processed_audio (np.ndarray): The preprocessed audio (Mel-spectrogram chunks) to be passed to the model.

        Returns:
            int: The index of the predicted genre in the self._genres list.
        """
        # Predict using model on processed data
        predictions =self._model.predict(processed_audio)
        # Get average prediction over all chunks in processed_audio's chunks
        average_predictions = np.mean(predictions, axis=0)
        # Get index of highest prediction category
        prediction_genre_index = np.argmax(average_predictions)
        return prediction_genre_index
    
    def predict_genre_chain(self, audio_path, target_shape=(150, 150)):
        """
        The full pipeline for predicting the genre of an audio file. This function handles loading the model,
        preprocessing the audio, and making the genre prediction.

        It first checks the format of the audio file, converts it to WAV if necessary, preprocesses it,
        and then uses the model to predict the genre.

        Args:
            audio_path (str): Path to the audio file to be predicted.
            target_shape (tuple): The target shape for resizing the Mel-spectrogram (default is (150, 150)).

        Returns:
            str: The predicted genre label (e.g., 'rock', 'pop').
            None: If there was an error in the process (e.g., if the model could not be loaded or audio failed to process).
        """
        # Check if audio file is .wav
        if audio_path.lower().endswith(".wav"):
            #print("\nFile is a WAV")
            self.copy_wav_to_folder(audio_path)
        elif audio_path.lower().endswith(".mp3"):
            #print("\nFile is a MP3")
            self.mp3_to_wav(audio_path)
        else:
            logging.error("File Not supported.")
            #print("\nFile is a NOT supported.")
            return None
        # use the model which is loaded in constructor as self._model
        # Preprocess the audio
        processed_audio = self.preprocess_audio(target_shape)
        if processed_audio is None:
            logging.error("Audio preprocessing failed.")
            print(f"Audio: {self._audio_path} \nAudio could not be read")
            return None
        # Make prediction
        genre_index = self.prediction(processed_audio)
        genre_label = self._genres[genre_index]
        return genre_label