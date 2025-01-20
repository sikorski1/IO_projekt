import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
import threading
import os
import time
import pyautogui
import cv2
import glob
import numpy as np
import queue
from GUI.audio import start_recording_audio, stop_recording_audio, init_transcription_queue, process_transcription_queue
from GUI.transcription import process_audio_file
import subprocess
from GUI.settings import Settings
from GUI.more import More
from GUI.setNames import SetNames
from fpdf import FPDF
from GUI.summary import summarize_text_gemini
from fpdf import FPDF, HTMLMixin
import unidecode

class MyFPDF(FPDF, HTMLMixin):
    pass

class ScreenRecorderGUI:
    def __init__(self):
        self.selected_language = "en-US"  # Default language
        self.is_recording = False
        self.red_dot = None
        self.filename = "Recording.avi"
        self.resolution = (1920, 1080)
        self.codec = cv2.VideoWriter_fourcc(*"XVID")
        self.storage_size = 0  # self.max_files_size converted to bytes
        self.audio_bps = 0
        self.video_bps = 0
        self.max_audio_time = 0
        self.max_video_time = 0
        self.defaultImg = os.getcwd() + r"/GUI/teams.png"

        # Set up the GUI window
        self.root = ttk.Window(themename="vapor")
        self.root.title("Screen Recorder")
        self.root.geometry("450x550")
        # Settings
        self.Settings = Settings(self.root, "teams", "0.1GB", 100, True)
        # More
        self.More = More(self.root)
        # SetNames
        self.SetNames = SetNames(self.root)
        self.audio_output_file_path = ""
        self.audio_thread = None
        self.stop_audio_event = threading.Event()  # Event to signal audio thread to stop

        # Initialize transcription queue and thread
        self.transcription_queue = queue.Queue()
        init_transcription_queue(self.transcription_queue)
        self.transcription_thread = threading.Thread(target=process_transcription_queue, args=(self.transcription_queue,), daemon=True)
        self.transcription_thread.start()

        self.create_widgets()
        self.root.after(200, self.update_status)
        self.root.mainloop()

    def create_widgets(self):
        # Recording Indicator
        tk.Label(self.root, text="Recording Status:", font=("Arial", 14)).pack(
            pady=20
        )
        self.red_dot = tk.Label(self.root, bg="gray", width=5, height=2)
        self.red_dot.pack(pady=10)

        # Kontener na przyciski Start i Stop
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=(20, 40))

        # Start Button
        start_button = tk.Button(
            control_frame,
            text="Start Recording",
            command=self.start_recording,
            bg="green",
            fg="white",
            width=15,
        )
        start_button.pack(side=tk.LEFT, padx=5)

        # Stop Button
        stop_button = tk.Button(
            control_frame,
            text="Stop Recording",
            command=self.stop_recording,
            bg="red",
            fg="white",
            width=15,
        )
        stop_button.pack(side=tk.LEFT, padx=5)

        # Language Selection
        tk.Label(self.root, text="Select Language:", font=("Arial", 12)).pack(pady=10)

        language_frame = tk.Frame(self.root)
        language_frame.pack()

        polish_button = tk.Button(
            language_frame,
            text="PL",
            command=lambda: self.select_language("pl"),
            width=10,
        )
        polish_button.pack(side=tk.LEFT, padx=10)

        english_button = tk.Button(
            language_frame,
            text="ENG",
            command=lambda: self.select_language("en-US"),
            width=10,
        )
        english_button.pack(side=tk.LEFT, padx=10)

        self.language_label = tk.Label(
            self.root,
            text=f"Selected Language: {self.selected_language}",
            font=("Arial", 8),
        )
        self.language_label.pack(pady=10)

        settings_frame = tk.Frame(self.root)
        settings_frame.pack(fill=tk.X, padx=10, pady=10)

        more_button = ttk.Button(
            settings_frame,
            text="More",
            bootstyle="success-outline",
            command=lambda: self.More.open_more_window(self.calculate_window_pos),
        )
        more_button.pack(side=tk.LEFT)
        settings_button = ttk.Button(
            settings_frame,
            text="Settings",
            bootstyle="light-outline",
            command=lambda: self.Settings.open_settings_window(
                self.calculate_window_pos
            ),
        )
        settings_button.pack(side=tk.RIGHT)

    def calculate_window_pos(self, window_width, window_height):
        root_width = self.root.winfo_width()
        root_height = self.root.winfo_height()
        root_x = self.root.winfo_x()
        root_y = self.root.winfo_y()
        pos_x = root_x + (root_width // 2) - (window_width // 2)
        pos_y = root_y + (root_height // 2) - (window_height // 2)
        return f"{window_width}x{window_height}+{pos_x}+{pos_y}"

    def update_status(self):
        """Update the status indicator for recording."""
        if self.is_recording:
            self.red_dot.config(bg="red")
        else:
            self.red_dot.config(bg="gray")
        self.root.after(200, self.update_status)

    def select_language(self, language):
        """Set the selected language."""
        self.selected_language = language
        self.language_label.config(
            text=f"Selected Language: {self.selected_language}",
        )

    def calculate_self_storage_size(self):
        # Storage size converted to bytes:
        if self.Settings.max_files_size == "0.1GB":
            self.storage_size = 0.1 * 1024 * 1024 * 1024
        elif self.Settings.max_files_size == "10GB":
            self.storage_size = 10 * 1024 * 1024 * 1024
        elif self.Settings.max_files_size == "5GB":
            self.storage_size = 5 * 1024 * 1024 * 1024
        else:
            self.storage_size = 3 * 1024 * 1024 * 1024

    def audio_storage_calculations(self):
        """
        Calculates the maximum recording time for a given maximum file size
        """
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
        cv2.imwrite(file_path, frame, [cv2.IMWRITE_JPEG_QUALITY, int(self.Settings.quality)])
        # Calculate bytes of 1 sec video withut audio
        self.video_bps = 4 * os.path.getsize(
            file_path
        )  # 4, bo Patryczek tak w komendzie wpisał, ale w funkcji record_screen tego nie zawarł, więc troche lipa imo
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
            files = glob.glob(os.path.join(data_dir, "*"))
            files_whiteboard = glob.glob(os.path.join(whiteboard_dir, "*"))
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
        # threading.Thread(target=start_recording_audio, daemon=True).start()
        threading.Thread(target=self.record_screen, daemon=True).start()  # Video thread

    def stop_recording(self):
        """Stop recording process, wait for transcription to finish, and generate PDF."""
        if not self.is_recording:
            messagebox.showinfo("Info", "No recording in progress!")
            return
        self.is_recording = False
        self.stop_audio_recording()

        # Ensure there are screenshots before running ffmpeg
        data_dir = os.path.join(os.getcwd(), "whiteboard_data")
        image_files = glob.glob(os.path.join(data_dir, "*.jpeg"))

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
        else:
            print("No screenshots captured.")

        # Wait for all transcription tasks to complete
        self.transcription_queue.join()

        self.generate_pdf_report(data_dir, output_dir, meeting_start_time)

        messagebox.showinfo("Info", "Recording saved")

    def count_jpeg_files_glob(self, folder_path="whiteboard_data"):
        """Zlicza liczbę plików JPEG w danym folderze używając glob."""
        if not os.path.isdir(folder_path):
            raise ValueError(f"Podana ścieżka '{folder_path}' nie jest folderem.")

        pattern = os.path.join(folder_path, "*.jpeg")  # Wzorzec dla plików .jpeg
        return len(glob.glob(pattern))

    def compare_frames(self, frame1, frame2):
        """
        Compares the current frame with the previous frame using absolute difference.
        """
        threshold = 60 # if threshold is higher than similarity than return true and save screenshot + split audio
        if frame1 is None or frame2 is None:
            # Handle cases where one or both frames are None (e.g., at the beginning)
            return 0.0

        # Resize frame2 to match the size of frame1 (if necessary)
        if frame1.shape != frame2.shape:
            frame2 = cv2.resize(frame2, (frame1.shape[1], frame1.shape[0]))

        # Convert to grayscale if not already
        if len(frame1.shape) == 3:
            frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        if len(frame2.shape) == 3:
            frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

        # Take the absolute difference of the images
        res = cv2.absdiff(frame1, frame2)

        # Convert the result to integer type
        res = res.astype(np.uint8)

        # Find percentage difference based on the number of pixels that are not zero
        percentage = (np.count_nonzero(res) * 100) / res.size

        return (100 - percentage) < threshold

    def record_screen(self):
        """Record the screen, save screenshots, and manage audio recording segments."""
        name = "screenshot"
        i = 0
        last_comparison_time = time.time()
        start_time = time.time()
        prev_frame = None

        # Start initial audio recording IMMEDIATELY:
        file_path_audio_initial = os.path.join(os.getcwd(), "whiteboard_data", f"{name}_whiteboard.{i}.wav")
        self.audio_output_file_path = file_path_audio_initial
        self.stop_audio_event.clear()
        self.audio_thread = threading.Thread(
            target=start_recording_audio,
            args=(
                file_path_audio_initial,
                self.stop_audio_event,
                self.selected_language,
                self.transcription_queue
            ),
            daemon=True,
        )
        self.audio_thread.start()

        while self.is_recording:
            try:
                jpeg_count = self.count_jpeg_files_glob()
                print(f"Number of JPEG files: {jpeg_count}")
            except ValueError as e:
                print(e)

            if (jpeg_count <= 4 * self.max_video_time and self.max_audio_time >= time.time() - start_time):
                img = pyautogui.screenshot()
                frame = np.array(img)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                file_path = os.path.join(os.getcwd(), "data", f"{name}.{i}.jpeg")
                file_path_whiteboard = os.path.join(os.getcwd(), "whiteboard_data", f"{name}_whiteboard.{i}.jpeg")

                current_time = time.time()

                if i == 0:
                    cv2.imwrite(file_path_whiteboard, frame, [cv2.IMWRITE_JPEG_QUALITY, int(self.Settings.quality)])
                elif current_time - last_comparison_time >= 1:
                    if prev_frame is not None and self.compare_frames(prev_frame, frame):
                        cv2.imwrite(file_path_whiteboard, frame, [cv2.IMWRITE_JPEG_QUALITY, int(self.Settings.quality)])
                        file_path_audio = os.path.join(os.getcwd(), "whiteboard_data", f"{name}_whiteboard.{i}.wav")
                        self.audio_output_file_path = file_path_audio

                        self.stop_audio_recording() # Stop previous audio segment
                        self.stop_audio_event.clear()
                        self.audio_thread = threading.Thread(
                            target=start_recording_audio,
                            args=(
                                file_path_audio,
                                self.stop_audio_event,
                                self.selected_language,
                                self.transcription_queue
                            ),
                            daemon=True,
                        )
                        self.audio_thread.start() # Start new audio segment
                    
                    prev_frame = frame.copy()
                    cv2.imwrite(file_path, frame, [cv2.IMWRITE_JPEG_QUALITY, int(self.Settings.quality)])
                    last_comparison_time = current_time

                i += 1
            elif jpeg_count > 4 * self.max_video_time:
                print("Max video time reached")
                self.stop_recording() # Stop recording if video limit reached
            else:
                print("Max audio time reached")
                self.stop_recording() # Stop recording if audio limit reached

    def stop_audio_recording(self):
        """Stops the currently running audio recording thread."""
        if self.audio_thread and self.audio_thread.is_alive():
            self.stop_audio_event.set()  # Signal the thread to stop
            self.audio_thread.join()  # Wait for the thread to finish
            self.audio_thread = None
    
    def generate_pdf_report(self, data_dir, output_dir, meeting_start_time):
        pdf = MyFPDF()
        pdf.set_title(f"Meeting Report {meeting_start_time}")
        pdf.set_author("Your App Name")
        pdf.set_font("helvetica", size=12) # Use a standard font


        for img_file in sorted(glob.glob(os.path.join(data_dir, "*.jpeg"))):
            pdf.add_page()
            pdf.image(img_file, x=10, y=10, w=190)

            txt_file = os.path.splitext(img_file)[0] + ".txt"
            if os.path.exists(txt_file):
                y_position = 150
                try:
                    with open(txt_file, "r", encoding="utf-8") as f:
                        text = f.read()

                        # Remove diacritics:
                        ascii_text = unidecode.unidecode(text)

                        pdf.set_xy(10, y_position)
                        pdf.multi_cell(0, 10, ascii_text)

                except Exception as e:
                    print(f"Error: {e}")
                    pdf.set_xy(10, y_position)
                    pdf.multi_cell(0, 10, f"Error processing text: {e}")


        summary_output_dir = os.path.join(output_dir, "summary_output")
        summary_file_path = summarize_text_gemini(data_dir, summary_output_dir, self.selected_language)

        if summary_file_path:
            pdf.add_page()
            pdf.set_font("helvetica", size=14)  # Or another standard font
            pdf.cell(0, 10, "Meeting Summary", ln=True, align="C")
            pdf.set_font("helvetica", size=12)  # Or another standard font

            y_position = 25
            try:
                with open(summary_file_path, "r", encoding="utf-8") as f:
                    summary_text = f.read()

                     # Remove diacritics:
                    ascii_summary = unidecode.unidecode(summary_text)

                    pdf.set_xy(10, y_position)
                    pdf.multi_cell(0, 10, ascii_summary) 
            except Exception as e:
                print(f"Error processing summary: {e}")
                pdf.set_xy(10, y_position)
                pdf.multi_cell(0, 10, f"Error processing summary: {e}")

        pdf_output_path = os.path.join(output_dir, f"{meeting_start_time}_report.pdf")
        pdf.output(pdf_output_path, "F")
        print(f"PDF report generated: {pdf_output_path}")