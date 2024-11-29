import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import os
import time
import pyautogui
import cv2
import numpy as np
import speech_recognition as sr
from .audio import start_recording_audio, stop_recording_audio  # Assuming you have this file with functions
from pydub import AudioSegment
from pydub.silence import split_on_silence

class ScreenRecorderGUI:
    def __init__(self):
        self.file_path = ""
        self.selected_language = ""
        self.is_recording = False
        self.red_dot = None
        self.transcription_thread = None
        self.filename = "Recording.avi"
        self.resolution = (1920, 1080)
        self.codec = cv2.VideoWriter_fourcc(*"XVID")
        self.fps = 30.0

        #Transcription Recorder
        self.r = sr.Recognizer()

        # Set up the GUI window
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

        transcript_button = tk.Button(file_transcript_frame, text="Transcript File", command=self.open_transcription_thread, bg="blue", fg="white", width=15)
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
        """Start the screen and audio recording process."""
        os.system("rm -r ./data/*")
        if self.is_recording:
            messagebox.showinfo("Info", "Recording is already in progress!")
            return
        self.is_recording = True

        # Start separate threads for audio recording and screen recording
        threading.Thread(target=start_recording_audio, daemon=True).start()  # Audio thread
        threading.Thread(target=self.record_screen, daemon=True).start()  # Video thread

    def stop_recording(self):
        """Stop recording process."""
        if not self.is_recording:
            messagebox.showinfo("Info", "No recording in progress!")
            return
        self.is_recording = False

        os.system("ffmpeg -y -framerate 4 -i ./data/screenshot.%d.png -c:v libx264 -pix_fmt yuv420p outfile.mkv")
        stop_recording_audio("output.wav")  # Assuming this stops audio recording
        
        os.system("ffmpeg -y -i outfile.mkv -i output.wav -c:v copy -c:a aac output.mp4 | y")

        messagebox.showinfo("Info", f"Recording saved as {self.filename}")

    def record_screen(self):
        """Record the screen and save it to a video file."""
        name = "screenshot"
        i = 0
        while self.is_recording:
            img = pyautogui.screenshot()
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            cv2.imwrite("./data/"+name+"."+str(i)+".png",frame)
            i+=1

    def open_transcription_thread(self):
        """Opens transcription thread"""
        if not self.file_path:
            self.file_path_label.config(text="No file selected")
            return
        if not self.selected_language:
            self.file_path_label.config(text="No language provided")
            return
        if not self.file_path.lower().endswith('.wav'):
            self.file_path_label.config(text="Invalid file type. Please select a .wav file.")
            return
        if self.transcription_thread and self.transcription_thread.is_alive():
            self.file_path_label.config(text="Transcription already in progress")
            return
        self.file_path_label.config(text="Transcription started...")
        self.transcription_thread = threading.Thread(target=self.perform_transcription)
        self.transcription_thread.start()

    def perform_transcription(self):
        """Perform transcription on the selected audio file."""
        try:
            filename = os.path.basename(self.file_path).rsplit('.', 1)[0]

            print("Transcription started...")
            start_time = time.time()

            transcription = self.get_full_file_transcription(self.file_path, filename)  

            elapsed_time = time.time() - start_time
            print(f"Transcription completed in {elapsed_time:.2f} seconds") 
            self.file_path_label.config(text=f"Transcription completed in {elapsed_time:.2f} seconds")
            with open(f"./IO_projekt/recorder/audio_transcriptions/{filename}.txt", "w", encoding="utf=8") as f:
                f.write(transcription)
        except Exception as e:
            print(f"Error during transcription: {e}")
            self.file_path_label.config(text=f"Error: {e}") 

    def get_single_chunk_transcription(self, path):
        """Returns single chunk text"""
        with sr.AudioFile(path) as source:
            audio_listened = self.r.record(source)
            text = self.r.recognize_google(audio_listened, language=self.selected_language)

        return text

    def get_full_file_transcription(self, path, filename):
        """Returns full file text"""
        sound = AudioSegment.from_file(path)
        #split when silence > 3000ms, 
        chunks = split_on_silence(sound, 
                              min_silence_len = 3000, silence_thresh=sound.dBFS-14, keep_silence=3000)
        folder_name = "./IO_projekt/recorder/audio_chunks/"
        os.makedirs(folder_name, exist_ok=True)

        whole_text=""

        for i, audio_chunk in enumerate(chunks, start=1):
            #create chunk in chunk folder
            chunk_filename = os.path.join(folder_name, f"{filename}_chunk{i}.wav")
            audio_chunk.export(chunk_filename, format="wav")
            try:
                self.file_path_label.config(text=f"Transcription {filename}_chunk{i} processing...")
                text = self.get_single_chunk_transcription(chunk_filename)
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                print(f"{filename}_chunk{i}.wav: {text} \n")
                whole_text += "\n"+text
            finally:
            #    Remove the chunk file after processing
                if os.path.exists(chunk_filename):
                    os.remove(chunk_filename)
                    print(f"Deleted chunk: {chunk_filename}")
        return whole_text
    

