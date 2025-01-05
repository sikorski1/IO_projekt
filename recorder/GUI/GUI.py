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
import speech_recognition as sr
from .audio import start_recording_audio, stop_recording_audio  # Assuming you have this file with functions
from fpdf import FPDF
from pydub import AudioSegment
from pydub.silence import split_on_silence
from tkinterPdfViewer import tkinterPdfViewer as pdf
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
        self.fps = 30.0
        self.platform = "teams"
        self.max_files_size = "10GB"
        self.defaultImg = os.getcwd() + r"/GUI/teams.png"
        #Transcription Recorder
        self.r = sr.Recognizer()

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

        transcript_button = tk.Button(self.root, text="Transcript File", command=self.open_transcription_thread, bg="blue", fg="white", width=15)
        transcript_button.pack(padx=5)
        # Przycisk Settings wyrównany do prawej strony
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
        self.settings_window.geometry(self.calculate_window_pos(250, 250))

        platforms = ["teams", "zoom", "meet"]
        max_files_size = ["10GB", "5GB", "3GB"]
        fps_options = ["30", "20", "15"]

        ttk.Label(self.settings_window, text="Platform:", bootstyle="info").pack(pady=5)
        self.platforms_var = ttk.StringVar(value=platforms[0])
        platforms_menu = ttk.Combobox(self.settings_window, textvariable=self.platforms_var, values=platforms, bootstyle="default")
        platforms_menu.pack()

        # Max File Size Dropdown
        ttk.Label(self.settings_window, text="Max File Size:", bootstyle="info").pack(pady=5)
        self.max_files_size_var = ttk.StringVar(value=max_files_size[0])
        max_files_size_menu = ttk.Combobox(self.settings_window, textvariable=self.max_files_size_var, values=max_files_size, bootstyle="default")
        max_files_size_menu.pack()

        # FPS Dropdown
        ttk.Label(self.settings_window, text="FPS:", bootstyle="info").pack(pady=5)
        self.fps_var = ttk.StringVar(value=fps_options[0])
        fps_menu = ttk.Combobox(self.settings_window, textvariable=self.fps_var, values=fps_options, bootstyle="default")
        fps_menu.pack()

    def save_settings(self):
        selected_platform = self.platforms_var.get()
        self.platform = selected_platform

        selected_max_file_size = self.max_files_size_var.get()
        self.max_files_size = selected_max_file_size
        
        selected_fps = self.fps_var.get()
        self.fps = selected_fps

        print(f"Settings saved:")
        print(f"Platform: {self.platform}")
        print(f"Max File Size: {self.max_files_size}")
        print(f"FPS: {self.fps}")

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

    def start_recording(self):
        """Start the screen and audio recording process."""
        data_dir = os.path.join(os.getcwd(), "data")
        whiteboard_dir = os.path.join(os.getcwd(), "whiteboard_data")

        # Remove all files in the directory
        if os.path.exists(data_dir):
            files = glob.glob(os.path.join(data_dir, '*'))
            files_whiteboard = glob.glob(os.path.join(whiteboard_dir, '*'))
            for file in files:
                os.remove(file)  # Remove individual files
            for file in files_whiteboard:
                os.remove(file)  # Remove whiteboard files
        else:
            print(f"Directory '{data_dir}' does not exist.")
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

        # Ensure there are screenshots before running ffmpeg
        data_dir = "./whiteboard_data" 
        if len(glob.glob(os.path.join(data_dir, '*.png'))) > 0:
            os.system(f"ffmpeg -y -framerate 4 -pattern_type glob -i '{data_dir}/*.png' -c:v libx264 -pix_fmt yuv420p ./out/whiteboard_video.mkv")
        else:
            print("No screenshots captured.")

        stop_recording_audio("./out/audio.wav")  # Assuming this stops audio recording

        # os.system("ffmpeg -y -i outfile.mkv -i output.wav -c:v copy -c:a aac output.mp4") // connect two files dont think it is neccessary

        messagebox.showinfo("Info", f"Recording saved as {self.filename}")

    def record_screen(self):
        """Record the screen and save it to a video file."""
        name = "screenshot"
        i = 0
        last_comparison_time = time.time()
        similarity = None
        while self.is_recording:
            img = pyautogui.screenshot()
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            file_path = os.path.join(os.getcwd(), "data", f"{name}.{i}.png")
            file_path_whiteboard = os.path.join(os.getcwd(), "whiteboard_data", f"{name}_whiteboard.{i}.png")
            current_time = time.time()
            if current_time - last_comparison_time >= 5: #every 5 sec check
                cv2.imwrite(file_path,frame)
                similarity = self.compare_img_with_default(file_path)
                print(f"Similarity with default image: {similarity:.2f}%")
                last_comparison_time = current_time
            if similarity is not None and similarity > 30: #similiarity set to 30%
                cv2.imwrite(file_path_whiteboard,frame)
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

