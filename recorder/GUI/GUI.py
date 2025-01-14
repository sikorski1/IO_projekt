import tkinter as tk
from tkinter import filedialog, messagebox, PhotoImage
import ttkbootstrap as ttk
import threading
import os
import time
import pyautogui
import cv2
import glob
import numpy as np
import json
import speech_recognition as sr
from .audio import start_recording_audio, stop_recording_audio  # Assuming you have this file with functions
from .transcription import process_audio_file
from fpdf import FPDF
from pydub import AudioSegment
from pydub.silence import split_on_silence
from tkinterPdfViewer import tkinterPdfViewer as pdf
import subprocess
class ScreenRecorderGUI:
    def __init__(self):
        self.file_path = ""
        self.file_txt_path=""
        self.file_pdf_path=""
        self.selected_language = ""
        self.is_recording = False
        self.red_dot = None
        self.transcription_thread = None
        self.filename = "Recording.avi"
        self.resolution = (1920, 1080)
        self.codec = cv2.VideoWriter_fourcc(*"XVID")
        self.platform = "teams"
        self.max_files_size = "0.1GB"
        self.storage_size = 0 # self.max_files_size converted to bytes
        self.quality = 100
        self.audio_bps = 0
        self.video_bps = 0
        self.max_audio_time = 0
        self.max_video_time = 0        
        self.defaultImg = os.getcwd() + r"/GUI/teams.png"\
        #Transcription
        self.speaker_recognition = 1 # 1 - enabled, 0 - disabled, SPEAKER RECOGNITION!!!

        # Set up the GUI window
        self.root = ttk.Window(themename="vapor")
        self.root.title("Screen Recorder")
        self.root.geometry("450x550")

        self.create_widgets()
        self.root.after(200, self.update_status)
        self.root.mainloop()

    def create_widgets(self):
        # Recording Indicator
        tk.Label(self.root, text="Recording Status:", font=("Arial", 14)).pack(pady=20)
        self.red_dot = tk.Label(self.root, bg="gray", width=5, height=2)
        self.red_dot.pack(pady=10)

        # Kontener na przyciski Start i Stop
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=(20, 40))

        # Start Button
        start_button = tk.Button(control_frame, text="Start Recording", command=self.start_recording, bg="green", fg="white", width=15)
        start_button.pack(side=tk.LEFT, padx=5)

        # Stop Button
        stop_button = tk.Button(control_frame, text="Stop Recording", command=self.stop_recording, bg="red", fg="white", width=15)
        stop_button.pack(side=tk.LEFT, padx=5)

        # File Path Input and Transcript Button
        ttk.Label(self.root, text="File Transcription", font=("Arial", 14)).pack(pady=10)

        ttk.Label(self.root, text="Select .wav file:", font=("Arial", 12)).pack(pady=10)
        file_path_button = tk.Button(self.root, text="Browse", command=self.select_file, bg="blue", fg="white", width=15)
        file_path_button.pack(padx=5)


        self.file_path_label = ttk.Label(self.root, text="No file selected", bootstyle="danger", font=("Arial", 8))
        self.file_path_label.pack(pady=5)

        # Language Selection
        ttk.Label(self.root, text="Select Language:", font=("Arial", 12)).pack(pady=10)

        language_frame = tk.Frame(self.root)
        language_frame.pack()

        polish_button = tk.Button(language_frame, text="PL", command=lambda: self.select_language("pl"), width=10)
        polish_button.pack(side=tk.LEFT, padx=10)

        english_button = tk.Button(language_frame, text="ENG", command=lambda: self.select_language("en-US"), width=10)
        english_button.pack(side=tk.LEFT, padx=10)

        self.language_label = ttk.Label(self.root, text="No language selected", bootstyle="danger", font=("Arial", 8))
        self.language_label.pack(pady=10)
        transcription_frame = tk.Frame(self.root)
        transcription_frame.pack(pady=10)
        transcript_button = tk.Button(transcription_frame, text="Transcript File", command=self.open_transcription_thread, bg="blue", fg="white", width=15)
        transcript_button.pack(padx=5)
        set_speaker_name_button = tk.Button(transcription_frame, text="Set names", command=self.open_set_name_window, bg="blue", fg="white", width=15)
        transcript_button.pack(side=tk.LEFT, padx=10)
        set_speaker_name_button.pack(side=tk.LEFT, padx=10)
        settings_frame = tk.Frame(self.root)
        settings_frame.pack(fill=tk.X, padx=10, pady=10)

        more_button = ttk.Button(settings_frame, text="More", bootstyle="success-outline", command=self.open_more_window)
        more_button.pack(side=tk.LEFT)
        settings_button = ttk.Button(settings_frame, text="Settings", bootstyle="light-outline", command=self.open_settings_window)
        settings_button.pack(side=tk.RIGHT)

    def calculate_window_pos(self, window_width, window_height):
        root_width = self.root.winfo_width()
        root_height = self.root.winfo_height()
        root_x = self.root.winfo_x()
        root_y = self.root.winfo_y()
        pos_x = root_x + (root_width // 2) - (window_width // 2)
        pos_y = root_y + (root_height // 2) - (window_height // 2)
        return f"{window_width}x{window_height}+{pos_x}+{pos_y}"
    
    def load_speakers(self):
        try:
            with open(os.getcwd() + r"/recorder/speaker_registry.json") as file:
                data = json.load(file)
                return list(data.keys())
        except(FileNotFoundError, json.JSONDecodeError):
            return []
        
    def save_speakers(self, data, original_names, entries):
        new_names = [entry.get() for entry in entries]
        updated_data = {new_name: data[speaker] for new_name, speaker in zip(new_names, original_names)}
    
        with open(os.getcwd() + r"/recorder/speaker_registry.json", "w") as file:
            json.dump(updated_data, file, indent=4)
    
        messagebox.showinfo("Zapisano", "Nazwy speakerów zostały zapisane.")

    def open_set_name_window(self):
        self.set_name_window = tk.Toplevel(self.root)
        self.set_name_window.title("Set Name")
        self.set_name_window.geometry(self.calculate_window_pos(350, 380))
        self.set_name_window.transient(self.root)
        self.set_name_window.grab_set()
        ttk.Label(self.set_name_window, text="Set recognised names", font=("Arial", 12)).pack(pady=5)

        container = tk.Frame(self.set_name_window)
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        canvas = tk.Canvas(container, width=150)
        scrollbar = tk.Scrollbar(container, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        # Konfiguracja scrollbara
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        data = {}
        original_names = self.load_speakers()
        entries = []
        
        if original_names:
            with open(os.getcwd() + r"/recorder/speaker_registry.json", "r") as file:
                data = json.load(file)

        for name in original_names:
            frame = tk.Frame(scrollable_frame)
            frame.pack(pady=2)

            label = tk.Label(frame, text="Speaker:")
            label.pack(side=tk.LEFT, padx=5)

            entry = tk.Entry(frame)
            entry.insert(0, name)  # Wstawia aktualną nazwę speakera
            entry.pack(side=tk.LEFT)
            entries.append(entry)

        button_frame = tk.Frame(self.set_name_window)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

        save_button = ttk.Button(button_frame, text="Save", bootstyle="outline", command=lambda: self.save_speakers(data, original_names, entries))
        save_button.pack(side=tk.RIGHT)

    def open_more_window(self):
        self.more_window = tk.Toplevel(self.root)
        self.more_window.title("More")
        self.more_window.geometry(self.calculate_window_pos(350, 350))
        self.more_window.transient(self.root)
        self.more_window.grab_set()
        ttk.Label(self.more_window, text="Txt to pdf coverter", font=("Arial", 12)).pack(pady=5)
        ttk.Label(self.more_window, text="Select .txt file:", font=("Arial", 10)).pack(pady=10)
        file_txt_path_button = tk.Button(self.more_window, text="Browse", command=self.select_txt_file, bg="blue", fg="white", width=15)
        file_txt_path_button.pack(padx=5)
        if self.file_txt_path:
            self.file_txt_path_label = ttk.Label(self.more_window, text=f"Selected: {self.file_txt_path}", bootstyle="success", font=("Arial", 8))
        else:
            self.file_txt_path_label = ttk.Label(self.more_window, text="No file selected", bootstyle="danger", font=("Arial", 8))
        self.file_txt_path_label.pack(pady=5)
        conversion_button = ttk.Button(self.more_window, text="Convert", bootstyle="primary", command=self.txt_to_pdf_conversion)
        conversion_button.pack(pady=(5,20))

        ttk.Label(self.more_window, text="Open pdf", font=("Arial", 12)).pack(pady=5)
        ttk.Label(self.more_window, text="Select .pdf file:", font=("Arial", 10)).pack(pady=10)
        file_pdf_path_button = tk.Button(self.more_window, text="Browse", command=self.select_pdf_file, bg="blue", fg="white", width=15)
        file_pdf_path_button.pack(padx=5)
        if self.file_pdf_path:
            self.file_pdf_path_label = ttk.Label(self.more_window, text=f"Selected: {self.file_pdf_path}", bootstyle="success", font=("Arial", 8))
        else:
            self.file_pdf_path_label = ttk.Label(self.more_window, text="No file selected", bootstyle="danger", font=("Arial", 8))
        self.file_pdf_path_label.pack(pady=5)
        open_pdf_button = ttk.Button(self.more_window, text="Open", bootstyle="primary", command=self.open_pdf)
        open_pdf_button.pack()

    def open_settings_window(self):
        self.settings_window = tk.Toplevel(self.root)
        self.settings_window.title("Settings")
        self.settings_window.geometry(self.calculate_window_pos(250, 350))
        self.settings_window.transient(self.root)
        self.settings_window.grab_set()
        platforms = ["teams", "zoom", "meet"]
        max_files_size = ["0.1GB", "10GB", "5GB", "3GB"]
        quality_options = ["100", "90", "80", "70", "60", "50", "40", "30", "20", "10"]

        ttk.Label(self.settings_window, text="Platform:", bootstyle="info").pack(pady=5)
        self.platforms_var = ttk.StringVar(value=platforms[0])
        platforms_menu = ttk.Combobox(self.settings_window, textvariable=self.platforms_var, values=platforms, bootstyle="default")
        platforms_menu.pack()

        # Max File Size Dropdown
        ttk.Label(self.settings_window, text="Max File Size:", bootstyle="info").pack(pady=5)
        self.max_files_size_var = ttk.StringVar(value=max_files_size[0])
        max_files_size_menu = ttk.Combobox(self.settings_window, textvariable=self.max_files_size_var, values=max_files_size, bootstyle="default")
        max_files_size_menu.pack()

        # Quality Dropdown
        ttk.Label(self.settings_window, text="Quality:", bootstyle="info").pack(pady=5)
        self.quality = ttk.StringVar(value=quality_options[0])
        quality_menu = ttk.Combobox(self.settings_window, textvariable=self.quality, values=quality_options, bootstyle="default")
        quality_menu.pack()

        ttk.Label(self.settings_window, text="Speaker Recognition:", bootstyle="info").pack(pady=5)
        self.recognition_var = tk.BooleanVar(value=self.speaker_recognition)
        switchButton = ttk.Checkbutton(
            self.settings_window,
            text="Enable Recognition",
            variable=self.recognition_var,
            bootstyle="switch"
        )
        switchButton.pack()
        button_frame = tk.Frame(self.settings_window)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        save_button = ttk.Button(button_frame, text="Save", bootstyle="outline", command=self.save_settings)
        save_button.pack(side=tk.RIGHT)

    def save_settings(self):
        selected_platform = self.platforms_var.get()
        self.platform = selected_platform

        selected_max_file_size = self.max_files_size_var.get()
        self.max_files_size = selected_max_file_size
        
        selected_quality = self.quality.get()
        self.self_quality = selected_quality

        selected_recognition = self.recognition_var.get()
        self.speaker_recognition = selected_recognition
        print(f"Settings saved:")
        print(f"Platform: {self.platform}")
        print(f"Max File Size: {self.max_files_size}")
        print(f"Quality: {self.quality}")
        print(f"Speaker Recognition: {self.speaker_recognition}")

        tk.messagebox.showinfo("Settings", "Settings have been saved successfully!")
        self.settings_window.destroy()
    def update_status(self):
        """Update the status indicator for recording."""
        if self.is_recording:
            self.red_dot.config(bg="red")
        else:
            self.red_dot.config(bg="gray")
        self.root.after(200, self.update_status)

    def compare_img_with_default(self, imgPath):
        """comparing two imgs with same resolution"""
        if self.platform == "teams":
            self.defaultImg = os.getcwd() + r"/GUI/teams.png"
        elif self.platform == "zoom":
            self.defaultImg = os.getcwd() + r"/GUI/zoom.png"
        else:
            self.defaultImg = os.getcwd() + r"/GUI/meet.png"

        img1 = cv2.imread(self.defaultImg, 0)
        img2 = cv2.imread(imgPath, 0)

        # Check if images are loaded correctly
        if img1 is None:
            raise FileNotFoundError(f"Default image not found at path: {self.defaultImg}")
        if img2 is None:
            raise FileNotFoundError(f"Image not found at path: {imgPath}")

        # Resize img2 to match the size of img1
        img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

        #--- take the absolute difference of the images ---
        res = cv2.absdiff(img1, img2)

        #--- convert the result to integer type ---
        res = res.astype(np.uint8)

        #--- find percentage difference based on the number of pixels that are not zero ---
        percentage = (np.count_nonzero(res) * 100)/ res.size

        return 100 - percentage
    
    def select_file(self):
        """Open a file dialog to select a file and store its path."""
        if self.transcription_thread and self.transcription_thread.is_alive():
            self.file_path_label.config(text="Transcription already in progress", bootstyle="danger")
            return
        self.file_path = filedialog.askopenfilename(filetypes=[("Audio files", "*.wav")])
        self.file_path_label.config(text=f"Selected: {self.file_path}", bootstyle="success")
    def select_txt_file(self):
        """Open a file dialog to select a txt file and store its path."""
        try:
            self.file_txt_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
            if self.file_txt_path:
                self.file_txt_path_label.config(text=f"Selected: {self.file_txt_path}", bootstyle="success")
            else:
                self.file_txt_path_label.config(text="No file selected", bootstyle="danger")
        except Exception as e:
            print(f"Error during file selection: {e}")
            messagebox.showerror("Error", f"An error occurred: {e}")
    def select_pdf_file(self):
        """Open a file dialog to select a pdf file and store its path."""
        try:
            self.file_pdf_path = filedialog.askopenfilename(filetypes=[("Pdf Files", "*.pdf")])
            if self.file_pdf_path:
                self.file_pdf_path_label.config(text=f"Selected: {self.file_pdf_path}", bootstyle="success")
            else:
                self.file_pdf_path_label.config(text="No file selected", bootstyle="danger")
        except Exception as e:
            print(f"Error during file selection: {e}")
            messagebox.showerror("Error", f"An error occurred: {e}")

    def select_language(self, language):
        """Set the selected language."""
        if self.transcription_thread and self.transcription_thread.is_alive():
            self.language_label.config(text="Transcription already in progress", bootstyle="danger")
            return
        self.selected_language = language
        self.language_label.config(text=f"Selected Language: {self.selected_language}", bootstyle="success")

    def calculate_self_storage_size(self):
        # Storage size converted to bytes:
        if self.max_files_size == "0.1GB":
            self.storage_size = 0.1 * 1024 * 1024 * 1024
        elif self.max_files_size == "10GB":
            self.storage_size = 10 * 1024 * 1024 * 1024
        elif self.max_files_size == "5GB":
            self.storage_size = 5 * 1024 * 1024 * 1024
        else:
            self.storage_size = 3 * 1024 * 1024 * 1024

    def audio_storage_calculations(self): # funkcja do przeliczania czasu nagrywania audio nie powinna w sumie być tu, ale tam nie ogarniam o co chodzi, to zostawiam tutaj
        """Calculates the maximum recording time for a given maximum file size"""
        self.calculate_self_storage_size()
        self.audio_bps = 48000 * 2 * 2  # 48000 samplerate, 2 channels, 2 bytes per sample
        self.max_audio_time = self.storage_size // self.audio_bps
        print(f"Max audio time: {self.max_audio_time} seconds")

    # Function to calculate the storage size of video
    def video_storage_calculations(self):
        # Sample screenshot to calculate number of screenshots
        name = "sample"
        sample_img = pyautogui.screenshot()
        frame = np.array(sample_img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        file_path = os.path.join(os.getcwd(), "data", f"{name}.jpeg")
        # Save the sample image
        cv2.imwrite(file_path,frame,[cv2.IMWRITE_JPEG_QUALITY, int(self.quality)])
        # Calculate bytes of 1 sec video withut audio
        self.video_bps = 4*os.path.getsize(file_path) # 4, bo Patryczek tak w komendzie wpisał, ale w funkcji record_screen tego nie zawarł, więc troche lipa imo
        # Calculate bytes per second
        self.max_video_time = self.storage_size // (self.video_bps)

    def start_recording(self):
        """Start the screen and audio recording process."""
        self.audio_storage_calculations()
        self.video_storage_calculations()
        data_dir = os.path.join(os.getcwd(), "data")
        whiteboard_dir = os.path.join(os.getcwd(), "whiteboard_data")

        # Remove all files in the directory
        if os.path.exists(data_dir):
            files = glob.glob(os.path.join(data_dir, '*'))
            files_whiteboard = glob.glob(os.path.join(whiteboard_dir, '*'))
            for file in files:
                os.remove(file)  # Remove individual files
                pass
            for file in files_whiteboard:
                os.remove(file)  # Remove whiteboard files
                pass
        else:
            print(f"Directory '{data_dir}' does not exist.")
        if self.is_recording:
            messagebox.showinfo("Info", "Recording is already in progress!")
            return
        self.is_recording = True

        # Start separate threads for audio recording and screen recording
        threading.Thread(target=start_recording_audio, daemon=True).start()     
        threading.Thread(target=self.record_screen, daemon=True).start()  # Video thread

    def stop_recording(self):
        """Stop recording process."""
        if not self.is_recording:
            messagebox.showinfo("Info", "No recording in progress!")
            return
        self.is_recording = False

        # Ensure there are screenshots before running ffmpeg
        data_dir = os.path.join(os.getcwd(), "whiteboard_data")
        image_files = glob.glob(os.path.join(data_dir, '*.jpeg'))
        
        if len(image_files) > 0:
            # Create a file list for ffmpeg
            file_list_path = os.path.join(data_dir, "file_list.txt")
            with open(file_list_path, "w") as file_list:
                for img_file in sorted(image_files):  # Ensure proper order
                    file_list.write(f"file '{img_file}'\n")
                    file_list.write(f"duration 0.25\n")

            # ffmpeg command using file list
            current_date = time.strftime("%Y-%m-%d")
            meeting_start_time = time.strftime("%H-%M-%S")
            output_dir = os.path.join(os.getcwd(), "..", "meetings", current_date)
            os.makedirs(output_dir, exist_ok=True)
            output_file = os.path.join(output_dir, f"{meeting_start_time}_whiteboard.mkv")
            output_file_audio = os.path.join(output_dir, f"{meeting_start_time}_audio.wav")
            ffmpeg_command = [
                "ffmpeg",
                "-y",
                "-f", "concat",
                "-safe", "0",
                "-i", file_list_path,
                "-framerate", "4",  # add a frame rate
                "-c:v", "libx264",
                "-pix_fmt", "yuv420p",
                output_file,
            ]
            subprocess.run(ffmpeg_command, check=True)
        else:
            print("No screenshots captured.")

        stop_recording_audio(output_file_audio)  # Assuming this stops audio recording

        messagebox.showinfo("Info", f"Recording saved as {self.filename}")
        
    def count_jpeg_files_glob(self, folder_path="whiteboard_data"):
        """Zlicza liczbę plików JPEG w danym folderze używając glob."""
        if not os.path.isdir(folder_path):
            raise ValueError(f"Podana ścieżka '{folder_path}' nie jest folderem.")

        pattern = os.path.join(folder_path, "*.jpeg")  # Wzorzec dla plików .jpeg
        return len(glob.glob(pattern))

    def record_screen(self):
        """Record the screen and save it to a video file."""
        name = "screenshot"
        i = 0
        last_comparison_time = time.time()
        start_time = time.time()
        similarity = None
        while self.is_recording:
            try:
                jpeg_count = self.count_jpeg_files_glob()
                print(f"Liczba plików JPEG: {jpeg_count}")
            except ValueError as e:
                print(e)
            if jpeg_count <= 4*self.max_video_time and self.max_audio_time >= time.time()-start_time:
                img = pyautogui.screenshot()
                frame = np.array(img)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                file_path = os.path.join(os.getcwd(), "data", f"{name}.{i}.jpeg")
                file_path_whiteboard = os.path.join(os.getcwd(), "whiteboard_data", f"{name}_whiteboard.{i}.jpeg")
                current_time = time.time()
                if current_time - last_comparison_time >= 5: #every 5 sec check
                    cv2.imwrite(file_path,frame,[cv2.IMWRITE_JPEG_QUALITY, int(self.quality)])
                    similarity = self.compare_img_with_default(file_path)
                    print(f"Similarity with default image: {similarity:.2f}%")
                    last_comparison_time = current_time
                if similarity is not None and similarity > 15: #similiarity set to
                    cv2.imwrite(file_path_whiteboard,frame,[cv2.IMWRITE_JPEG_QUALITY, int(self.quality)])
                i+=1
            elif jpeg_count > 4*self.max_video_time:
                print("Max video time reached")
                self.stop_recording()
                self.is_recording = False
            else:
                print("Max audio time reached")
                print(time.time()-start_time)
                self.stop_recording()
                self.is_recording = False

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
        self.transcription_thread = threading.Thread(target=process_audio_file, args=[self.file_path, self.speaker_recognition])
        self.transcription_thread.start()
        self.transcription_thread.join()
        self.file_path_label.config(text="")
        tk.messagebox.showinfo("Info","Finished transcription thread")


    # def perform_transcription(self):
    #     """Perform transcription on the selected audio file."""
    #     try:
    #         filename = os.path.basename(self.file_path).rsplit('.', 1)[0]

    #         print("Transcription started...")
    #         start_time = time.time()

    #         transcription = self.get_full_file_transcription(self.file_path, filename)  

    #         elapsed_time = time.time() - start_time
    #         print(f"Transcription completed in {elapsed_time:.2f} seconds") 
    #         self.file_path_label.config(text=f"Transcription completed in {elapsed_time:.2f} seconds")
    #         with open(f"./audio_transcriptions/{filename}.txt", "w", encoding="utf=8") as f:
    #             f.write(transcription)
    #     except Exception as e:
    #         print(f"Error during transcription: {e}")
    #         self.file_path_label.config(text=f"Error: {e}") 

    # def get_single_chunk_transcription(self, path):
    #     """Returns single chunk text"""
    #     with sr.AudioFile(path) as source:
    #         audio_listened = self.r.record(source)
    #         text = self.r.recognize_google(audio_listened, language=self.selected_language)

    #     return text

    # def get_full_file_transcription(self, path, filename):
    #     """Returns full file text"""
    #     sound = AudioSegment.from_file(path)
    #     #split when silence > 3000ms, 
    #     chunks = split_on_silence(sound, 
    #                           min_silence_len = 3000, silence_thresh=sound.dBFS-14, keep_silence=3000)
    #     folder_name = "./audio_chunks/"
    #     os.makedirs(folder_name, exist_ok=True)

    #     whole_text=""

    #     for i, audio_chunk in enumerate(chunks, start=1):
    #         #create chunk in chunk folder
    #         chunk_filename = os.path.join(folder_name, f"{filename}_chunk{i}.wav")
    #         audio_chunk.export(chunk_filename, format="wav")
    #         try:
    #             self.file_path_label.config(text=f"Transcription {filename}_chunk{i} processing...")
    #             text = self.get_single_chunk_transcription(chunk_filename)
    #         except sr.UnknownValueError as e:
    #             print("Error:", str(e))
    #         else:
    #             text = f"{text.capitalize()}. "
    #             print(f"{filename}_chunk{i}.wav: {text} \n")
    #             whole_text += "\n"+text
    #         finally:
    #         #    Remove the chunk file after processing
    #             if os.path.exists(chunk_filename):
    #                 os.remove(chunk_filename)
    #                 print(f"Deleted chunk: {chunk_filename}")
    #     return whole_text
    
    def txt_to_pdf_conversion(self):
        if not self.file_txt_path:
            tk.messagebox.showerror("Error", "No .txt file selected!")
            return
        output_pdf_path = self.file_txt_path.rsplit('.', 1)[0] + ".pdf"
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size = 12)
            with open(self.file_txt_path, "r", encoding="utf-8") as file:
                for line in file:
                    words = line.strip().split() 
                    while words:
                        segment = words[:15] 
                        words = words[15:] 
                        pdf.cell(200, 10, txt=" ".join(segment), ln=True)

            pdf.output(output_pdf_path)
            tk.messagebox.showinfo("Success", f"PDF saved as {output_pdf_path}")
            self.file_txt_path = ""
            self.file_txt_path_label.config(text="No file selected", bootstyle="danger")
        except Exception as e:
            tk.messagebox.showerror("Error", f"An error occurred: {e}")

    def open_pdf(self):
        if not self.file_pdf_path:
            tk.messagebox.showerror("Error", "No PDF file selected!")
            return

        if not os.path.exists(self.file_pdf_path):

            tk.messagebox.showerror("Error", "PDF file not found!")
            return
        self.pdf_window = tk.Toplevel(self.more_window)
        self.pdf_window.title("PDF Viewer")
        self.pdf_window.geometry(self.calculate_window_pos(600, 600))
    
        d = pdf.ShowPdf().pdf_view(self.pdf_window, pdf_location=self.file_pdf_path, width=100, height=100)
        d.pack(expand=True, fill="both")
        self.file_pdf_path = ""
        self.file_pdf_path_label.config(text="No file selected", bootstyle="danger")
