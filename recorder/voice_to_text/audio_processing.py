import subprocess

def extract_audio(mp4_path, output_path):
    """
    Wyodrębnia ścieżkę audio z pliku MP4 i zapisuje ją jako plik WAV.
    """
    command = [
        "ffmpeg", "-i", mp4_path, "-ar", "16000", "-ac", "1", output_path
    ]
    subprocess.run(command, check=True)
    print(f"Audio extracted to {output_path}")
