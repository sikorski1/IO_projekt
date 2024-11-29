import tkinter as tk
from tkinter import filedialog
import speech_recognition as sr
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
import threading
import time
class ScreenRecorderGUI:
    def __init__(self):
        self.file_path = ""
        self.selected_language = ""
        self.is_recording = False
        self.red_dot = None
        self.transcription_thread = None

        self.root = tk.Tk()
        self.root.title("Screen Recorder")
        self.root.geometry("400x400")

        self.create_widgets()
        self.root.after(200, self.update_status)
        self.root.mainloop()

    def create_widgets(self):
        # Start Button
        start_button = tk.Button(self.root, text="Start Recording", command=self.start_recording, bg="green", fg="white", width=20)
        start_button.pack(pady=10)

        # Stop Button
        stop_button = tk.Button(self.root, text="Stop Recording", command=self.stop_recording, bg="red", fg="white", width=20)
        stop_button.pack(pady=10)

        # Recording Indicator
        tk.Label(self.root, text="Recording Status:").pack(pady=10)
        self.red_dot = tk.Label(self.root, bg="gray", width=5, height=2)
        self.red_dot.pack()

        # File Path Input and Transcript Button
        file_transcript_frame = tk.Frame(self.root)
        file_transcript_frame.pack(pady=10)

        file_path_button = tk.Button(file_transcript_frame, text="Browse", command=self.select_file, bg="blue", fg="white", width=15)
        file_path_button.pack(side=tk.LEFT, padx=5)

        transcript_button = tk.Button(file_transcript_frame, text="Transcript File", command=self.transcript_file, bg="blue", fg="white", width=15)
        transcript_button.pack(side=tk.LEFT, padx=5)

        self.file_path_label = tk.Label(self.root, text="No file selected")
        self.file_path_label.pack(pady=5)

        # Language Selection
        tk.Label(self.root, text="Select Language:").pack(pady=10)

        language_frame = tk.Frame(self.root)
        language_frame.pack()

        polish_button = tk.Button(language_frame, text="PL", command=lambda: self.select_language("pl"), width=10)
        polish_button.pack(side=tk.LEFT, padx=10)

        english_button = tk.Button(language_frame, text="ENG", command=lambda: self.select_language("en-US"), width=10)
        english_button.pack(side=tk.LEFT, padx=10)

        self.language_label = tk.Label(self.root, text="No language selected")
        self.language_label.pack(pady=10)

    def update_status(self):
        """Update the status indicator for recording."""
        if self.is_recording:
            self.red_dot.config(bg="red")
        else:
            self.red_dot.config(bg="gray")
        self.root.after(200, self.update_status)

    def select_file(self):
        """Open a file dialog to select a file and store its path."""
        self.file_path = filedialog.askopenfilename(title="Select a File")
        self.file_path_label.config(text=f"Selected: {self.file_path}")

    def select_language(self, language):
        """Set the selected language."""
        self.selected_language = language
        self.language_label.config(text=f"Selected Language: {self.selected_language}")

    def start_recording(self):
        """Start recording process."""
        if self.is_recording:
            return
        self.is_recording = True

    def stop_recording(self):
        """Stop recording process."""
        if not self.is_recording:
            return
        self.is_recording = False

    def transcript_file(self):
        if not self.file_path:
            self.file_path_label.config(text="No file selected")
            return
        if not self.file_path.lower().endswith('.wav'):
            self.file_path_label.config(text="Invalid file type. Please select a .wav file.")
            return
        if self.transcription_thread and self.transcription_thread.is_alive():
            self.file_path_label.config(text="Transcription already in progress")
            return

        self.transcription_thread = threading.Thread(target=self.perform_transcription)
        self.transcription_thread.start()
    def perform_transcription(self):
        try:
            file_name_without_extension = os.path.basename(self.file_path).rsplit('.', 1)[0]
            r = sr.Recognizer()
            with sr.AudioFile(self.file_path) as source:
                audio_data = r.record(source)
                print("Transcription started...")
                start_time = time.time()
                text = r.recognize_google(audio_data, language=self.selected_language)

            print(f"File name: {file_name_without_extension}")
            elapsed_time = time.time() - start_time
            print(f"Transcription completed in {elapsed_time:.2f} seconds")
            print(f"Transcription: {text}")
        except Exception as e:
            print(f"Error during transcription: {e}")
