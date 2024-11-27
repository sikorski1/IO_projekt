import pyautogui
import cv2
import numpy as np
import threading
import tkinter as tk
from .audio import start_recording_audio, stop_recording_audio
from tkinter import messagebox

# Specify resolution
resolution = (1920, 1080)

# Specify video codec and filename
codec = cv2.VideoWriter_fourcc(*"XVID")
filename = "Recording.avi"
fps = 30.0  # Reduced for smoother performance

# Flag for recording state
is_recording = False
video_writer = None


def start_recording():
    global is_recording, video_writer

    if is_recording:
        messagebox.showinfo("Info", "Recording is already in progress!")
        return

    is_recording = True
    video_writer = cv2.VideoWriter(filename, codec, fps, resolution)

    # Start a separate thread for screen recording
    threading.Thread(target=start_recording_audio, daemon=True).start()
    threading.Thread(target=record_screen, daemon=True).start()

def stop_recording():
    global is_recording, video_writer

    if not is_recording:
        messagebox.showinfo("Info", "No recording is in progress!")
        return

    is_recording = False
    if video_writer:
        video_writer.release()
        stop_recording_audio("output.wav")
        video_writer = None
        
    messagebox.showinfo("Info", f"Recording saved as {filename}")


def record_screen():
    global is_recording, video_writer

    while is_recording:
        # Take a screenshot
        img = pyautogui.screenshot()

        # Convert the screenshot to a numpy array
        frame = np.array(img)

        # Convert it from BGR to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Write it to the video file
        video_writer.write(frame)

# Create the GUI
def create_gui():
    def update_status():
        """Update the status indicator for recording."""
        if is_recording:
            red_dot.config(bg="red")
        else:
            red_dot.config(bg="gray")
        root.after(200, update_status)

    root = tk.Tk()
    root.title("Screen Recorder")
    root.geometry("300x200")

    # Start Button
    start_button = tk.Button(root, text="Start Recording", command=start_recording, bg="green", fg="white", width=20)
    start_button.pack(pady=10)

    # Stop Button
    stop_button = tk.Button(root, text="Stop Recording", command=stop_recording, bg="red", fg="white", width=20)
    stop_button.pack(pady=10)

    # Recording Indicator
    tk.Label(root, text="Recording Status:").pack(pady=10)
    global red_dot
    red_dot = tk.Label(root, bg="gray", width=5, height=2)
    red_dot.pack()

    # Status updater
    root.after(200, update_status)

    root.mainloop()
