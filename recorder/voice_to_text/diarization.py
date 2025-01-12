from pyannote.audio import Pipeline

def diarize_audio(audio_path, model_name="pyannote/speaker-diarization"):
    """
    Przeprowadza diarization dla podanego pliku audio.
    """
    pipeline = Pipeline.from_pretrained(model_name)
    diarization_result = pipeline(audio_path)
    return diarization_result
