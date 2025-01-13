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
_pipeline = None
_speaker_recognition = None
_model = None
_sample_rate = 16000
_similarity_threshold = 0.55
_margin_of_safety = 0.005
_speaker_registry_file = "speaker_registry.json"
_speaker_recognition_enabled = True  # New global variable to control speaker recognition

def initialize_transcription(speaker_registry_file="speaker_registry.json",
                             sample_rate=16000,
                             similarity_threshold=0.55, margin_of_safety=0.005):
    # Load environment variables from .env file
    load_dotenv()
    api_key = os.getenv("API_KEY")

    # Konfiguracja cache
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

    # Inicjalizacja modeli
    _pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization", use_auth_token=api_key)
    _speaker_recognition = SpeakerRecognition.from_hparams(
        source="speechbrain/spkrec-ecapa-voxceleb",
        savedir=os.path.join(os.environ["PYANNOTE_CACHE"],
                            "speechbrain_speaker_rec"))
    _model = whisper.load_model("large-v2")


# Zarządzanie bazą speakerów
def load_speaker_registry():
    if os.path.exists(_speaker_registry_file):
        with open(_speaker_registry_file, 'r') as f:
            return json.load(f)
    return {}

def save_speaker_registry(speaker_registry):
    with open(_speaker_registry_file, 'w') as f:
        json.dump(speaker_registry, f, indent=4)

# Funkcja hashująca embeddingi
def hash_embedding(embedding):
    return hashlib.sha256(embedding.tobytes()).hexdigest()

# Funkcja do identyfikacji mówcy
def identify_speaker(embedding, speaker_registry):
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
        # Uśrednienie embeddingów z mniejszą wagą dla nowego embeddingu
        speaker_registry[best_match_id]["embedding"] = (
            np.array(speaker_registry[best_match_id]["embedding"]) * 0.8 + embedding * 0.2
        ).tolist()
        return best_match_id

    # Dodanie nowego mówcy
    new_speaker_id = f"SPEAKER_{len(speaker_registry) + 1:02}"
    speaker_registry[new_speaker_id] = {
        "embedding": embedding.tolist(),
        "embedding_hash": embedding_hash
    }
    return new_speaker_id

# Funkcja do diarizacji i transkrypcji
def diarize_and_transcribe(audio_segment, speaker_registry, enable_speaker_recognition):
    diarization = _pipeline(
        {"uri": "audio", "waveform": torch.tensor(audio_segment).unsqueeze(0), "sample_rate": _sample_rate})
    segments = []

    for segment, _, label in diarization.itertracks(yield_label=True):
        start, end = segment.start, segment.end
        if (end - start) < 1:  # Pomijanie bardzo krótkich segmentów
            continue

        segment_audio = audio_segment[int(start * _sample_rate):int(end * _sample_rate)]
        
        if enable_speaker_recognition:
            embedding = _speaker_recognition.encode_batch(
                torch.tensor(segment_audio).unsqueeze(0)).squeeze(0).detach().cpu().numpy()
            speaker_id = identify_speaker(embedding, speaker_registry)
        else:
            speaker_id = "SPEAKER" # Default speaker ID if disabled
        
        segments.append({"start": start, "end": end, "speaker": speaker_id})

    return segments

# Zapis transkrypcji do pliku
def save_transcription(segments, transcription_filename, audio_data):
    with open(transcription_filename, "a", encoding="utf-8") as txtfile:
        if not segments:
            txtfile.write("Nie udało się zidentyfikować segmentów.\n")
            return
        for segment in tqdm(segments, desc="Transcribing segments"):
            start_time = segment['start']
            end_time = segment['end']
            speaker_id = segment['speaker']
            segment_audio = audio_data[int(start_time * _sample_rate):int(end_time * _sample_rate)]
            transcription = _model.transcribe(segment_audio, fp16=True)['text']
            txtfile.write(f"{speaker_id} [{start_time:.2f}s - {end_time:.2f}s]: {transcription.strip()}\n")

# Funkcja do konwersji audio do 16 kHz
def convert_audio_to_16k(audio_data, original_sr, target_sr=16000):
    if original_sr == target_sr:
        return audio_data  # Nothing to do

    resampled_audio = librosa.resample(y=audio_data, orig_sr=original_sr, target_sr=target_sr)
    return resampled_audio

# Przetwarzanie pliku audio
def process_audio_file(file_path, enable_speaker_recognition=1, output_16k_path=None):
    initialize_transcription()
    global _speaker_recognition_enabled
    _speaker_recognition_enabled = bool(enable_speaker_recognition)
    print(f"Przetwarzanie pliku audio: {file_path}, Rozpoznawanie mówców: {'Włączone' if _speaker_recognition_enabled else 'Wyłączone'}")

    try:
        audio_data, sr = librosa.load(file_path, sr=None)  # Load with original sample rate
    
        # Resample to 16k before diarization
        audio_16k = convert_audio_to_16k(audio_data, sr, 16000)
    
        speaker_registry = load_speaker_registry()
        segments = diarize_and_transcribe(audio_16k, speaker_registry, _speaker_recognition_enabled)  # Pass the flag to diarize function
        if _speaker_recognition_enabled:
            save_speaker_registry(speaker_registry)

    
        # Generate transcription filename in the same directory as the audio file
        audio_dir = os.path.dirname(file_path)
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        transcription_filename = os.path.join(audio_dir, f"{base_name}.txt")
    
        if segments:
            save_transcription(segments, transcription_filename, audio_16k)
            print(f"Transkrypcja zapisana do: {transcription_filename}")

        else:
            print("Nie udało się przeprowadzić diarizacji.")

        if output_16k_path:
            sf.write(output_16k_path, audio_16k, 16000)  # Save the resampled audio to disk
            print(f"Audio resampled and saved to: {output_16k_path}")

    except Exception as e:
        print(f"Błąd przetwarzania pliku audio: {e}")