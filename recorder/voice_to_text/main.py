from audio_processing import extract_audio
from transciber import transcribe_audio
from diarization import diarize_audio
from utils import ensure_folder_exists

def main():
    input_video = "voice_to_text/input.mp4"
    audio_output = "voice_to_text/outputs/audio.wav"
    transcript_output = "voice_to_text/outputs/transcript.txt"

    # Upewnij się, że folder outputs istnieje
    ensure_folder_exists("outputs")

    # 1. Wyodrębnij audio
    extract_audio(input_video, audio_output)

    # 2. Transkrybuj audio
    transcription = transcribe_audio(audio_output)
    with open(transcript_output, "w", encoding='utf-8') as f:
        f.write(transcription)

    # 3. Diarization
    diarization_result = diarize_audio(audio_output)
    print(diarization_result)

if __name__ == "__main__":
    main()
