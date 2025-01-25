import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
import os
import json

class SetNames:
    def __init__(self, root):
        """
        Initializes the SetNames class.

        Args:
            root: The main tkinter application window.
        """
        self.root_window = root
        pass

    def open_set_name_window(self, calculate_window_pos):
        """
        Opens the window for setting speaker names.

        Args:
            calculate_window_pos: A function to calculate the window position.
        """
        # Creates a new window (Toplevel)
        self.set_name_window = tk.Toplevel(self.root_window)
        self.set_name_window.title("Set Name")
        # Sets the window geometry
        self.set_name_window.geometry(calculate_window_pos(350, 380))
        # Sets the window as dependent on the main window
        self.set_name_window.transient(self.root_window)
        # Captures all events, preventing interaction with the main window
        self.set_name_window.grab_set()
        # Creates an information label
        ttk.Label(self.set_name_window, text="Set recognised names", font=("Arial", 12)).pack(pady=5)

        # Container for content with a scrollbar
        container = tk.Frame(self.set_name_window)
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Creates Canvas and Scrollbar
        canvas = tk.Canvas(container, width=150)
        scrollbar = tk.Scrollbar(container, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        # Configures the scrollbar
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # Creates a window in the Canvas
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Places the canvas and scrollbar in the container
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Initializes data and a list of entries
        data = {}
        original_names = self.load_speakers()
        entries = []
        
        # Loads data from speaker_registry.json if it exists
        if original_names:
            with open(os.getcwd() + r"/speaker_registry.json", "r") as file:
                data = json.load(file)

        # Creates frames, labels, and entry fields for each speaker
        for name in original_names:
            frame = tk.Frame(scrollable_frame)
            frame.pack(pady=2)

            label = tk.Label(frame, text="Speaker:")
            label.pack(side=tk.LEFT, padx=5)

            entry = tk.Entry(frame)
            entry.insert(0, name)  # Inserts the current speaker name
            entry.pack(side=tk.LEFT)
            entries.append(entry)

        # Creates a frame for the buttons
        button_frame = tk.Frame(self.set_name_window)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

        # Creates a save button
        save_button = ttk.Button(button_frame, text="Save", bootstyle="outline", command=lambda: self.save_speakers(data, original_names, entries))

        save_button.pack(side=tk.RIGHT)

    def load_speakers(self):
        """
        Loads speaker names from the JSON file.

        Returns:
            list: A list of speaker names, or an empty list if the file doesn't exist or is empty.
        """
        try:
            with open(os.getcwd() + r"/speaker_registry.json") as file:
                data = json.load(file)
                return list(data.keys())
        except(FileNotFoundError, json.JSONDecodeError):
            return []

    def save_speakers(self, data, original_names, entries):
        """
        Saves the modified speaker names to the JSON file.

        Args:
            data (dict): A dictionary containing speaker data (unchanged names and other data).
            original_names (list): A list of the original speaker names.
            entries (list): A list of Entry objects, containing the new names.
        """
        # Gets the new names from the Entry fields
        new_names = [entry.get() for entry in entries]
        # Creates an updated dictionary
        updated_data = {new_name: data[speaker] for new_name, speaker in zip(new_names, original_names)}
        try:
            # Saves the updated dictionary to the JSON file
            with open(os.getcwd() + r"/speaker_registry.json", "w") as file:
                json.dump(updated_data, file, indent=4)
        except(FileNotFoundError, json.JSONDecodeError):
            # Displays an error message if an exception occurs
            messagebox.showinfo(FileNotFoundError, json.JSONDecodeError)
        
        # Displays a message indicating successful data saving
        messagebox.showinfo("Saved", "The names of the speakers have been saved")