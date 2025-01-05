import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np

# Global variables to store recording state and audio data  
recording = False
audio_data = []

def start_recording_audio(samplerate=48000, channels=2, duration=None):
    """
    Start recording audio. This function records audio continuously until `stop_recording`
    is called or the specified duration is reached.
    
    :param samplerate: Sampling rate (Hz). Default: 44100 (CD quality).
    :param channels: Number of audio channels. Default: 2 (stereo).
    :param duration: Duration of recording in seconds. If None, recording continues until stopped.
    """
    global recording, audio_data

    if recording:
        raise RuntimeError("Recording is already in progress!")


    print(sd.query_devices())

    print("Recording started...")
    recording = True
    audio_data = []

    # Record in chunks to avoid memory overflow
    def callback(indata, frames, time, status):
        if recording:
            audio_data.append(indata.copy())
        else:
            raise sd.CallbackStop

    with sd.InputStream(samplerate=samplerate, channels=channels, callback=callback, device=3): # change for loopback interface 
        if duration:
            sd.sleep(int(duration * 1000))
            stop_recording_audio()  # Automatically stop after duration
        else:
            while recording:
                sd.sleep(100)

def stop_recording_audio(output_file=None):
    """
    Stop recording audio and optionally save it to a file.

    :param output_file: Path to the output WAV file. If None, data will not be saved.
    :return: NumPy array of audio data.
    """
    global recording, audio_data

    recording = False
    print("Recording stopped.")

    # Concatenate chunks into a single NumPy array
    audio_data = np.concatenate(audio_data, axis=0)

    # Save to file if specified
    if output_file:
        write(output_file, 48000, (audio_data * 32767).astype(np.int16))  # 44100 Hz sample rate
        print(f"Audio saved to {output_file}")

    return audio_data
