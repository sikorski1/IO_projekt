import os
import torch
import numpy as np
import json
from pyannote.audio import Pipeline
from speechbrain.pretrained import SpeakerRecognition
from speechbrain.inference import SpeakerRecognition
from sklearn.metrics.pairwise import cosine_similarity
import hashlib
import librosa
from tqdm import tqdm
import whisper
import soundfile as sf
from dotenv import load_dotenv

# Global variables to hold the models (initialized once)
_pipeline = None  # Pyannote pipeline for speaker diarization
_speaker_recognition = None  # SpeechBrain model for speaker recognition
_model = None  # Whisper model for transcription
_sample_rate = 16000  # Target sample rate for audio processing
_similarity_threshold = 0.55  # Threshold for speaker similarity
_margin_of_safety = 0.005 # Margin for comparing similarity scores
_speaker_registry_file = "speaker_registry.json"  # File path for speaker registry
_speaker_recognition_enabled = True  # Flag to enable/disable speaker recognition


def initialize_transcription(speaker_registry_file="speaker_registry.json",
                             sample_rate=16000,
                             similarity_threshold=0.55, margin_of_safety=0.005):
    """
    Initializes the transcription pipeline by loading models and setting parameters.

    Args:
        speaker_registry_file (str): File path for the speaker registry.
        sample_rate (int): Target sample rate for audio processing.
        similarity_threshold (float): Threshold for speaker similarity.
        margin_of_safety (float): Margin for comparing similarity scores.
    """
    # Load environment variables from .env file
    load_dotenv()
    api_key = os.getenv("API_KEY")

    # Configure cache directories
    venv_dir = os.path.dirname(os.path.abspath(__file__))
    custom_cache_dir = os.path.join(venv_dir, "cache")
    os.environ["HF_HOME"] = os.path.join(custom_cache_dir, "huggingface")
    os.environ["TORCH_HOME"] = os.path.join(custom_cache_dir, "torch")
    os.environ["PYANNOTE_CACHE"] = os.path.join(custom_cache_dir, "pyannote")
    os.makedirs(os.environ["HF_HOME"], exist_ok=True)
    os.makedirs(os.environ["TORCH_HOME"], exist_ok=True)
    os.makedirs(os.environ["PYANNOTE_CACHE"], exist_ok=True)

    global _pipeline, _speaker_recognition, _model, _sample_rate, _similarity_threshold, _margin_of_safety, _speaker_registry_file
    _speaker_registry_file = speaker_registry_file
    _sample_rate = sample_rate
    _similarity_threshold = similarity_threshold
    _margin_of_safety = margin_of_safety

    # Initialize models
    _pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization", use_auth_token=api_key)
    _speaker_recognition = SpeakerRecognition.from_hparams(
        source="speechbrain/spkrec-ecapa-voxceleb",
        savedir=os.path.join(os.environ["PYANNOTE_CACHE"],
                            "speechbrain_speaker_rec"))
    _model = whisper.load_model("large-v2")

# Speaker registry management
def load_speaker_registry():
    """
    Loads the speaker registry from a JSON file.

    Returns:
        dict: The speaker registry or an empty dictionary if the file doesn't exist.
    """
    if os.path.exists(_speaker_registry_file):
        with open(_speaker_registry_file, 'r') as f:
            return json.load(f)
    return {}

def save_speaker_registry(speaker_registry):
    """
    Saves the speaker registry to a JSON file.

    Args:
        speaker_registry (dict): The speaker registry to be saved.
    """
    with open(_speaker_registry_file, 'w') as f:
        json.dump(speaker_registry, f, indent=4)

# Function to hash embeddings
def hash_embedding(embedding):
    """
    Hashes a speaker embedding to a unique identifier.

    Args:
        embedding (np.ndarray): The embedding to hash.

    Returns:
        str: The hashed embedding.
    """
    return hashlib.sha256(embedding.tobytes()).hexdigest()

# Function to identify speaker
def identify_speaker(embedding, speaker_registry):
    """
    Identifies a speaker based on an embedding and the speaker registry.

    Args:
        embedding (np.ndarray): The speaker embedding.
        speaker_registry (dict): The speaker registry.

    Returns:
        str: The speaker ID or None if the embedding is invalid.
    """
    if embedding is None:
        return None

    embedding_hash = hash_embedding(embedding)
    best_match_id = None
    max_similarity = 0
    second_best_similarity = 0

    for speaker_id, speaker_data in speaker_registry.items():
        if "embedding" in speaker_data:
            similarity = cosine_similarity(
                np.array(speaker_data["embedding"]).reshape(1, -1),
                embedding.reshape(1, -1)
            )[0][0]

            if similarity > max_similarity:
                second_best_similarity = max_similarity
                max_similarity = similarity
                best_match_id = speaker_id

    if max_similarity > _similarity_threshold and (
            max_similarity - second_best_similarity) > _margin_of_safety:
        # Average embeddings with less weight to the new embedding
        speaker_registry[best_match_id]["embedding"] = (
            np.array(speaker_registry[best_match_id]["embedding"]) * 0.8 + embedding * 0.2
        ).tolist()
        return best_match_id

    # Add new speaker
    new_speaker_id = f"SPEAKER_{len(speaker_registry) + 1:02}"
    speaker_registry[new_speaker_id] = {
        "embedding": embedding.tolist(),
        "embedding_hash": embedding_hash
    }
    return new_speaker_id

# Function for diarization and transcription
def diarize_and_transcribe(audio_segment, speaker_registry, enable_speaker_recognition):
    """
    Performs speaker diarization and transcription for a given audio segment.

    Args:
        audio_segment (np.ndarray): The audio segment.
        speaker_registry (dict): The speaker registry.
        enable_speaker_recognition (bool): Flag to enable or disable speaker recognition

    Returns:
        list: A list of segments with start and end times, speaker IDs.
    """
    diarization = _pipeline(
        {"uri": "audio", "waveform": torch.tensor(audio_segment).unsqueeze(0), "sample_rate": _sample_rate})
    segments = []

    for segment, _, label in diarization.itertracks(yield_label=True):
        start, end = segment.start, segment.end
        if (end - start) < 1:  # Skip very short segments
            continue

        segment_audio = audio_segment[int(start * _sample_rate):int(end * _sample_rate)]

        if enable_speaker_recognition:
            embedding = _speaker_recognition.encode_batch(
                torch.tensor(segment_audio).unsqueeze(0)).squeeze(0).detach().cpu().numpy()
            speaker_id = identify_speaker(embedding, speaker_registry)
        else:
            speaker_id = "SPEAKER" # Default speaker ID if recognition is disabled
            
        segments.append({"start": start, "end": end, "speaker": speaker_id})

    return segments

# Save transcription to a file
def save_transcription(segments, transcription_filename, audio_data):
    """
    Saves the transcription to a text file.

    Args:
        segments (list): A list of segments with start and end times, speaker IDs.
        transcription_filename (str): Path to the output text file.
        audio_data (np.ndarray): Audio data.
    """
    with open(transcription_filename, "a", encoding="utf-8") as txtfile:
        if not segments:
            txtfile.write("Failed to identify segments.\n")
            return
        for segment in tqdm(segments, desc="Transcribing segments"):
            start_time = segment['start']
            end_time = segment['end']
            speaker_id = segment['speaker']
            segment_audio = audio_data[int(start_time * _sample_rate):int(end_time * _sample_rate)]
            transcription = _model.transcribe(segment_audio, fp16=True)['text']
            txtfile.write(f"{speaker_id} [{start_time:.2f}s - {end_time:.2f}s]: {transcription.strip()}\n")


# Function to convert audio to 16 kHz
def convert_audio_to_16k(audio_data, original_sr, target_sr=16000):
    """
    Converts audio to 16 kHz sample rate.

    Args:
        audio_data (np.ndarray): The audio data.
        original_sr (int): The original sample rate.
        target_sr (int): The target sample rate (default is 16000 Hz).

    Returns:
         np.ndarray: The resampled audio data.
    """
    if original_sr == target_sr:
        return audio_data  # Nothing to do

    resampled_audio = librosa.resample(y=audio_data, orig_sr=original_sr, target_sr=target_sr)
    return resampled_audio

# Process audio file
def process_audio_file(file_path, selected_language, output_txt_path, enable_speaker_recognition=1):
    """
    Processes an audio file for diarization and transcription.

    Args:
        file_path (str): Path to the input audio file.
        selected_language (str): Selected language for transcription.
        output_txt_path (str): Path to the output text file.
        enable_speaker_recognition (int): Flag to enable/disable speaker recognition. 1 for enable, 0 for disable.
    """
    initialize_transcription()
    global _speaker_recognition_enabled
    _speaker_recognition_enabled = bool(enable_speaker_recognition)
    print(f"Processing audio file: {file_path}, Speaker recognition: {'Enabled' if _speaker_recognition_enabled else 'Disabled'}")

    try:
        audio_data, sr = librosa.load(file_path, sr=None)  # Load with original sample rate
    
        # Resample to 16k before diarization
        audio_16k = convert_audio_to_16k(audio_data, sr, 16000)
    
        speaker_registry = load_speaker_registry()
        segments = diarize_and_transcribe(audio_16k, speaker_registry, _speaker_recognition_enabled)  # Pass the flag to diarize function
        if _speaker_recognition_enabled:
            save_speaker_registry(speaker_registry)
    
        if segments:
            save_transcription(segments, output_txt_path, audio_16k)
            print(f"Transcription saved to: {output_txt_path}")

        else:
            print("Diarization failed.")

    except Exception as e:
        print(f"Error processing audio file: {e}")