import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import threading

# Global variables to manage recording state and audio data
recording = False
audio_data = []
audio_lock = threading.Lock()  # Lock for thread-safe access to audio_data
stop_event = threading.Event()

def start_recording_audio(file_path_audio, stop_event, samplerate=48000, channels=2):
    """
    Starts recording audio in a separate thread until the stop_event is set.

    :param file_path_audio: Path to save the recorded audio file.
    :param stop_event: A threading.Event to signal when to stop recording.
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
    device_id = None
    for i, device in enumerate(devices):
        if device['max_input_channels'] == 2:
            device_id = i
            break

    if device_id is None:
        raise RuntimeError("No suitable device found with 2 input channels.")

    print(f"Using device {device_id}: {devices[device_id]['name']}")
    
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
        device=device_id,
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
              write(file_path_audio, samplerate, (audio_array * 32767).astype(np.int16))
              print(f"Audio saved to {file_path_audio}")
          else:
              print("No audio data to save.")

    print("Recording stopped.")

def stop_recording_audio(output_file=None):
    """
    Stops the audio recording.

    :param output_file: Optional. If provided, the audio data will be saved to this file.
    """
    global recording
    
    # Signal the recording thread to stop
    stop_event.set()