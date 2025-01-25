import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import threading
import queue
import os
from GUI.transcription import process_audio_file

# Global variables to manage recording state and audio data
recording = False
audio_data = []
audio_lock = threading.Lock()  # Lock for thread-safe access to audio_data
stop_event = threading.Event()
transcription_queue = None

def init_transcription_queue(queue):
    global transcription_queue
    transcription_queue = queue

def process_transcription_queue(transcription_queue):
    """
    Continuously processes the transcription queue.
    """
    while True:
        try:
            # Get a transcription task from the queue
            wav_file, txt_file, selected_language = transcription_queue.get()

            # Process the transcription
            print(f"Transcribing {wav_file} to {txt_file} in {selected_language}")
            process_audio_file(wav_file, selected_language, txt_file)
            print(f"Transcription of {wav_file} saved to {txt_file}")

            # Mark the task as done
            transcription_queue.task_done()
        except Exception as e:
            print(f"Error transcribing {wav_file}: {e}")

def start_recording_audio(file_path_audio, stop_event, selected_language, transcription_queue, samplerate=48000, channels=2):
    """
    Starts recording audio in a separate thread until the stop_event is set.

    :param file_path_audio: Path to save the recorded audio file.
    :param stop_event: A threading.Event to signal when to stop recording.
    :param selected_language: The selected language for transcription.
    :param samplerate: Sampling rate in Hz. Default: 48000.
    :param channels: Number of audio channels. Default: 2 (stereo).
    """
    global recording, audio_data

    if recording:
        print("Recording is already in progress!")
        return

    devices = sd.query_devices()
    print(devices)

    # Find the device with 2 input channels
    selected_device = None
    for device in devices:
        if device['max_input_channels'] == 2:
            selected_device = device
            break

    if selected_device is None:
        raise RuntimeError("No suitable device found with 2 input channels.")

    print(f"Using device: {selected_device['name']}")

    recording = True
    audio_data = []

    def callback(indata, frames, time, status):
        """Callback function for audio recording."""
        if status:
            print(status)
        if not stop_event.is_set():
            with audio_lock:
                audio_data.append(indata.copy())
        else:
            raise sd.CallbackStop  # Stop the stream when the event is set

    with sd.InputStream(
        samplerate=samplerate,
        channels=channels,
        callback=callback,
        device=int(selected_device['index']),
    ):
        print("Recording started...")
        while not stop_event.is_set():
            sd.sleep(100)

    # Stop the recording
    recording = False

    # Save the audio data to a file after acquiring the lock
    if file_path_audio:
        with audio_lock:
            if audio_data:  # Check if audio_data is not empty
                audio_array = np.concatenate(audio_data, axis=0)
                write(
                    file_path_audio,
                    samplerate,
                    (audio_array * 32767).astype(np.int16),
                )
                print(f"Audio saved to {file_path_audio}")

                # Add the transcription task to the queue
                txt_file = os.path.splitext(file_path_audio)[0] + ".txt"
                transcription_queue.put((file_path_audio, txt_file, selected_language))

            else:
                print("No audio data to save.")

    print("Recording stopped.")
