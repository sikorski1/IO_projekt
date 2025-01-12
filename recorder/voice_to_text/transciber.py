import whisper

def transcribe_audio(audio_path, model_name="base"):
    """
    Transkrybuje plik audio za pomocą modelu Whisper.
    """
    model = whisper.load_model(model_name)
    result = model.transcribe(audio_path)
    return result["text"]
