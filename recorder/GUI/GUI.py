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
from GUI.audio import start_recording_audio, init_transcription_queue, process_transcription_queue
from GUI.transcription import process_audio_file
from GUI.more import More
from GUI.setNames import SetNames
from fpdf import FPDF
from GUI.summary import summarize_text_gemini
from fpdf import FPDF, HTMLMixin
import unidecode

class MyFPDF(FPDF, HTMLMixin):
    """
    Custom PDF class that inherits from FPDF and HTMLMixin for more capabilities.
    """
    pass

class ScreenRecorderGUI:
    """
    A class that provides a graphical user interface (GUI) for screen recording.
    """
    def __init__(self):
        """
        Initializes the ScreenRecorderGUI object, sets up the GUI, and defines necessary variables.
        """
        self.selected_language = "en-US"  # Default language for transcription
        self.is_recording = False  # Boolean to track recording state
        self.red_dot = None # TK Label to indicate the recording state
        self.filename = "Recording.avi"  # Default filename for video recording
        self.resolution = (1920, 1080)  # Default resolution for video
        self.codec = cv2.VideoWriter_fourcc(*"XVID")  # Default codec for video
        self.defaultImg = os.getcwd() + r"/GUI/teams.png" # Path to default image


        # Set up the GUI window
        self.root = ttk.Window(themename="vapor") # Initialize the main window
        self.root.title("Screen Recorder") # Set window title
        self.root.geometry("450x550") # Set window dimensions
        settings_frame = tk.Frame(self.root) # Create a frame for settings buttons
        settings_frame.pack(fill=tk.X, padx=10, pady=10) # Pack the settings frame into the main window
        
        # Threshold selection
        ttk.Label(settings_frame, text="Threshold:", bootstyle="info").pack(pady=5)
        self.threshold_var = tk.IntVar(value=80)
        threshold_menu = ttk.Combobox(settings_frame, textvariable=self.threshold_var, values=list(range(0, 101, 5)), bootstyle="default")
        threshold_menu.pack()

        # Settings Button
        set_names_button = ttk.Button(
            settings_frame,
            text="Set Names",
            bootstyle="info-outline",
            command=lambda: self.set_names.open_set_name_window(self.calculate_window_pos),
        ) # Initialize a button to open the set name dialog window
        set_names_button.pack(side=tk.RIGHT, padx=5) # Pack the set names button into the settings frame
        self.set_names = SetNames(self.root) # Initialize a class to set the speakers name

        # More button
        self.More = More(self.root) # Initialize more functions class
        # SetNames
        self.SetNames = SetNames(self.root)
        self.audio_output_file_path = ""  # Initialize a variable to keep track of audio output file path
        self.audio_thread = None  # Initialize a variable to keep track of the audio recording thread
        self.stop_audio_event = threading.Event()  # Event to signal audio thread to stop

        # Initialize transcription queue and thread
        self.transcription_queue = queue.Queue() # Create a queue to hold the audio paths for transcriptions
        init_transcription_queue(self.transcription_queue) # Initialize the transcription queue in the audio module
        self.transcription_thread = threading.Thread(target=process_transcription_queue, args=(self.transcription_queue,), daemon=True) # Initialize a thread for processing transcription queue
        self.transcription_thread.start() # Start the transcription thread

        self.create_widgets() # Call the method to create all widgets
        self.root.after(200, self.update_status) # Update the recoring state label
        self.root.mainloop() # Start the main loop to run the tkinter window

    def create_widgets(self):
        """
        Creates and packs all the GUI widgets including the recording indicator, start/stop buttons,
        language selection, and settings buttons.
        """
        # Recording Indicator
        tk.Label(self.root, text="Recording Status:", font=("Arial", 14)).pack(
            pady=20
        ) # Create a label for recording status
        self.red_dot = tk.Label(self.root, bg="gray", width=5, height=2) # Create a label to indicate current recording status
        self.red_dot.pack(pady=10)  # Pack the red dot status label

        # Button Frame for Start and Stop
        control_frame = tk.Frame(self.root) # Create a frame to pack the start and stop buttons
        control_frame.pack(pady=(20, 40)) # Pack the control frame

        # Start Button
        start_button = ttk.Button(
            control_frame,
            text="Start Recording",
            bootstyle="success-outline",
            command=self.start_recording,
            width=15,
        ) # Create start button
        start_button.pack(side=tk.LEFT, padx=5)  # Pack the start button into the control frame
        
        # Stop Button
        stop_button = ttk.Button(
            control_frame,
            text="Stop Recording",
            bootstyle="success-outline",
            command=self.stop_recording,
            width=15,
        ) # Create stop button
        stop_button.pack(side=tk.LEFT, padx=5) # Pack the stop button into the control frame

        # Language Selection
        tk.Label(self.root, text="Select Language:", font=("Arial", 12)).pack(pady=10) # Create a label to prompt for language selection

        language_frame = tk.Frame(self.root) # Create a frame for language buttons
        language_frame.pack() # Pack the language frame

        # Polish Button
        polish_button = ttk.Button(
            language_frame,
            text="PL",
            bootstyle="success-outline",
            command=lambda: self.select_language("pl"),
            width=10,
        ) # Create polish language button
        polish_button.pack(side=tk.LEFT, padx=10) # Pack polish language button into language frame

        # English Button
        english_button = ttk.Button(
            language_frame,
            text="ENG",
            bootstyle="success-outline",
            command=lambda: self.select_language("en-US"),
            width=10,
        )  # Create english language button
        english_button.pack(side=tk.LEFT, padx=10)  # Pack english language button into the language frame

        # Label to display selected language
        self.language_label = tk.Label(
            self.root,
            text=f"Selected Language: {self.selected_language}",
            font=("Arial", 8),
        ) # Create a label to display currently selected language
        self.language_label.pack(pady=10) # Pack the language label into the root window

        # Settings Buttons frame
        settings_frame = tk.Frame(self.root) # Create a settings frame to hold the setting buttons
        settings_frame.pack(fill=tk.X, padx=10, pady=10)  # Pack the settings frame into the root window

        # More button
        more_button = ttk.Button(
            settings_frame,
            text="More",
            bootstyle="success-outline",
            command=lambda: self.More.open_more_window(self.calculate_window_pos),
        ) # Create a button to open more settings window
        more_button.pack(side=tk.LEFT)  # Pack the more button to the settings frame

    def calculate_window_pos(self, window_width, window_height):
        """
        Calculates the position of a new window relative to the main window.

        Args:
            window_width (int): Width of the new window.
            window_height (int): Height of the new window.

        Returns:
            str: String representation of the geometry for the new window.
        """
        # Get the root window properties
        root_width = self.root.winfo_width()
        root_height = self.root.winfo_height()
        root_x = self.root.winfo_x()
        root_y = self.root.winfo_y()
        # Calculate x and y position of the window for centring
        pos_x = root_x + (root_width // 2) - (window_width // 2)
        pos_y = root_y + (root_height // 2) - (window_height // 2)
        # return formated string to display the window correctly
        return f"{window_width}x{window_height}+{pos_x}+{pos_y}"

    def update_status(self):
        """
        Updates the recording status indicator (red dot).
        """
        if self.is_recording:
            self.red_dot.config(bg="red") # if recording is active set the label to red
        else:
            self.red_dot.config(bg="gray") # if recording is not active set the label to gray
        self.root.after(200, self.update_status) # Keep calling this function to update the recording state

    def select_language(self, language):
        """
        Sets the selected language for transcription and updates the language label.

        Args:
            language (str): The language code ("pl" for Polish, "en-US" for English).
        """
        self.selected_language = language # Set selected language
        self.language_label.config(
            text=f"Selected Language: {self.selected_language}",
        ) # Update the label to display currently selected language

    def start_recording(self):
         """
        Starts the screen and audio recording processes, including cleaning old data
        from data folder and ensuring multiple recordings are not initiated at the same time.
        """
         # Set up the data directory where screenshots will be saved
         data_dir = os.path.join(os.getcwd(), "data")
         whiteboard_dir = os.path.join(os.getcwd(), "whiteboard_data")

         # Remove all files in the directory
         if os.path.exists(data_dir):
             files = glob.glob(os.path.join(data_dir, "*")) # Get all file paths in data directory
             files_whiteboard = glob.glob(os.path.join(whiteboard_dir, "*")) # Get all file paths in whiteboard directory
             for file in files:
                 os.remove(file)  # Remove individual files
                 pass
             for file in files_whiteboard:
                 os.remove(file)  # Remove whiteboard files
                 pass
         else:
             print(f"Directory '{data_dir}' does not exist.") # if directory doesn't exist, print message
         if self.is_recording:
             messagebox.showinfo("Info", "Recording is already in progress!") # if already recording show message box
             return
         self.is_recording = True # Set the is_recording variable to True

         # Start separate threads for audio recording and screen recording
         # threading.Thread(tfarget=start_recording_audio, daemon=True).start() # audio thread
         threading.Thread(target=self.record_screen, daemon=True).start()  # Video thread

    def stop_recording(self):
        """
        Stops the recording process, waits for all transcription tasks to finish,
        and generates a PDF report from the recorded data.
        """
        if not self.is_recording:
            messagebox.showinfo("Info", "No recording in progress!")
            return
        self.is_recording = False # Set the recording variable to false to stop recording
        self.stop_audio_recording() # Stop audio recording

        # Ensure there are screenshots before running ffmpeg
        data_dir = os.path.join(os.getcwd(), "whiteboard_data")
        image_files = glob.glob(os.path.join(data_dir, "*.jpeg")) # Search for all files in whiteboard directory

        if len(image_files) > 0: # if there are files in the directory do this:
            # Create a file list for ffmpeg
            file_list_path = os.path.join(data_dir, "file_list.txt") # path to the file
            with open(file_list_path, "w") as file_list: # open file for writing
                for img_file in sorted(image_files):  # Ensure proper order
                    file_list.write(f"file '{img_file}'\n") # add line to the file for the file path of image
                    file_list.write(f"duration 0.25\n") # add duration of each frame to the file

            # ffmpeg command using file list
            current_date = time.strftime("%Y-%m-%d") # get the current date
            meeting_start_time = time.strftime("%H-%M-%S") # get the current time
            output_dir = os.path.join(os.getcwd(), "..", "meetings", current_date) # set output directory to be created
            os.makedirs(output_dir, exist_ok=True) # create directory
        else:
            print("No screenshots captured.") # if no screenshots are present, print this

        # Wait for all transcription tasks to complete
        self.transcription_queue.join()

        self.generate_pdf_report(data_dir, output_dir, meeting_start_time) # generate pdf report

        messagebox.showinfo("Info", "Recording saved")

    def count_jpeg_files_glob(self, folder_path="whiteboard_data"):
        """
        Counts the number of JPEG files in a given folder using glob.

        Args:
            folder_path (str, optional): The folder path to search in. Defaults to "whiteboard_data".

        Returns:
            int: The number of JPEG files in the specified folder.

        Raises:
             ValueError: if the folder path is invalid
        """
        if not os.path.isdir(folder_path):
            raise ValueError(f"Podana ścieżka '{folder_path}' nie jest folderem.")

        pattern = os.path.join(folder_path, "*.jpeg")  # Wzorzec dla plików .jpeg
        return len(glob.glob(pattern)) # return the number of all files in the directory with the .jpeg extension

    def compare_frames(self, frame1, frame2):
        """
        Compares the current frame with the previous frame using absolute difference.

        Args:
             frame1 (np.ndarray): The first frame (usually the previous frame).
             frame2 (np.ndarray): The second frame (usually the current frame).
        Returns:
            bool: True if the frames are different, False otherwise.
        """
        threshold = self.threshold_var.get() # if threshold is higher than similarity than return true and save screenshot + split audio
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
        
        print("percentage: ", 100-percentage, " threshold: ", threshold)
        return (100 - percentage) < threshold

    def record_screen(self):
        """
        Records the screen, saves screenshots, and manages audio recording segments.
        """
        name = "screenshot" # generic name for screenshots and audio files
        i = 0 # variable to enumerate the filenames
        last_comparison_time = time.time() # Variable that keeps last time of frame comparison
        start_time = time.time()  # track start time of recording
        prev_frame = None  # variable to store the previous frame

        # Start initial audio recording IMMEDIATELY:
        file_path_audio_initial = os.path.join(os.getcwd(), "whiteboard_data", f"{name}_whiteboard.{i}.wav") # set path of the initial audio recording
        self.audio_output_file_path = file_path_audio_initial # assign initial audio path to the class variable
        self.stop_audio_event.clear() # clear the stop audio flag
        self.audio_thread = threading.Thread(
            target=start_recording_audio,
            args=(
                file_path_audio_initial,
                self.stop_audio_event,
                self.selected_language,
                self.transcription_queue
            ),
            daemon=True,
        ) # Initialize audio recording thread
        self.audio_thread.start() # start audio thread

        while self.is_recording: # Keep recording while the flag is True
            try:
                jpeg_count = self.count_jpeg_files_glob()  # Count all jpeg images in the whiteboard directory
                print(f"Number of JPEG files: {jpeg_count}") # Print the number of current screenshots
            except ValueError as e:
                print(e) # print error if there is some
            img = pyautogui.screenshot() # Get the screenshot
            frame = np.array(img) # change screenshot to array
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # convert the color of the frame to RGB for usage

            file_path = os.path.join(os.getcwd(), "data", f"{name}.{i}.jpeg") # set path of the screenshot for the data directory
            file_path_whiteboard = os.path.join(os.getcwd(), "whiteboard_data", f"{name}_whiteboard.{i}.jpeg") # set path of the screenshot for the whiteboard directory

            if i == 0 or (prev_frame is not None and self.compare_frames(prev_frame, frame)): # Compare frames after each screenshot
                cv2.imwrite(file_path_whiteboard, frame, [cv2.IMWRITE_JPEG_QUALITY, 100])  # Save the screenshot to the whiteboard data folder
                file_path_audio = os.path.join(os.getcwd(), "whiteboard_data", f"{name}_whiteboard.{i}.wav") # Set the file path for audio output
                self.audio_output_file_path = file_path_audio # Assign audio path to class variable
                
                self.stop_audio_recording()  # Stop previous audio segment
                self.stop_audio_event.clear() # clear the stop audio flag
                self.audio_thread = threading.Thread(
                    target=start_recording_audio,
                    args=(
                        file_path_audio,
                        self.stop_audio_event,
                        self.selected_language,
                        self.transcription_queue
                    ),
                    daemon=True,
                )  # initialize new audio recording thread for the new segment
                self.audio_thread.start()  # Start new audio segment
            
            prev_frame = frame.copy() # Copy current frame to previous frame variable for next comparison
            cv2.imwrite(file_path, frame, [cv2.IMWRITE_JPEG_QUALITY, 100]) # Save current screenshot in the data directory
            time.sleep(2)
            i += 1  # increase the index by 1

    def stop_audio_recording(self):
         """Stops the currently running audio recording thread."""
         if self.audio_thread and self.audio_thread.is_alive(): # if audio thread is active
             self.stop_audio_event.set()  # Signal the thread to stop
             self.audio_thread.join()  # Wait for the thread to finish
             self.audio_thread = None # set the audio_thread to None since it has finished

    def generate_pdf_report(self, data_dir, output_dir, meeting_start_time):
        """
        Generates a PDF report containing images, transcriptions, and a summary.

        Args:
            data_dir (str): Path to the directory where screenshots are stored.
            output_dir (str): Path to the directory where the PDF will be saved.
            meeting_start_time (str): Timestamp of the meeting start time for naming the PDF.
        """
        pdf = MyFPDF() # create PDF object
        pdf.set_title(f"Meeting Report {meeting_start_time}") # set PDF title
        pdf.set_author("Your App Name") # set PDF author
        pdf.set_font("helvetica", size=12) # set default font for the PDF

        for img_file in sorted(glob.glob(os.path.join(data_dir, "*.jpeg"))): # loop through all the images in the data folder
            pdf.add_page() # add a new page for each image
            pdf.image(img_file, x=10, y=10, w=190) # add image to pdf

            txt_file = os.path.splitext(img_file)[0] + ".txt" # create a text path from the screenshot path
            if os.path.exists(txt_file): # if the corresponding txt file is present
                y_position = 150 # set the y position of the text
                try:
                    with open(txt_file, "r", encoding="utf-8") as f: # open text file for reading
                        text = f.read() # read all text from txt file
                        
                        # Remove diacritics:
                        ascii_text = unidecode.unidecode(text) # remove diacritics from text for compatibility

                        pdf.set_xy(10, y_position) # set x and y position for the text
                        pdf.multi_cell(0, 10, ascii_text) # add the text to the PDF

                except Exception as e: # if error while opening or reading text file
                    print(f"Error: {e}") # print the error in the console
                    pdf.set_xy(10, y_position) # set the position for the error message
                    pdf.multi_cell(0, 10, f"Error processing text: {e}") # add the error message to the PDF

        summary_output_dir = os.path.join(output_dir, "summary_output") # set the output directory for the summary
        summary_file_path = summarize_text_gemini(data_dir, summary_output_dir, self.selected_language) # Summarize all the text files in data directory

        if summary_file_path: # if a summary was created
            pdf.add_page() # add a new page for summary
            pdf.set_font("helvetica", size=14)  # Or another standard font  set font for title
            pdf.cell(0, 10, "Meeting Summary", ln=True, align="C") # Add a title to the summary page
            pdf.set_font("helvetica", size=12)  # Or another standard font # set font for the summary

            y_position = 25 # set the y position of the text
            try:
                with open(summary_file_path, "r", encoding="utf-8") as f: # open summary file for reading
                    summary_text = f.read() # read summary from file
                    
                    # Remove diacritics:
                    ascii_summary = unidecode.unidecode(summary_text) # remove diacritics from summary for compatibility

                    pdf.set_xy(10, y_position) # set x and y position for the summary
                    pdf.multi_cell(0, 10, ascii_summary)  # add the summary to the PDF
            except Exception as e: # if there was an error while reading or processing summary file
                print(f"Error processing summary: {e}") # print error in the console
                pdf.set_xy(10, y_position) # set y position for the error message
                pdf.multi_cell(0, 10, f"Error processing summary: {e}")  # add error message to PDF

        pdf_output_path = os.path.join(output_dir, f"{meeting_start_time}_report.pdf") # set the path of the output pdf file
        pdf.output(pdf_output_path, "F") # output the pdf to the set path
        print(f"PDF report generated: {pdf_output_path}")  # print success message to the console