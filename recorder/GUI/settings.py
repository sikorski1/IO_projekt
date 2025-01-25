import tkinter as tk
import ttkbootstrap as ttk

class Settings:
    """
    A class to manage application settings, such as quality and speaker recognition.
    """
    def __init__(self, root, quality, recognition):
        """
        Initializes the Settings class.

        Args:
            root (tk.Tk): The main tkinter application window.
            quality (str): Initial quality setting.
            recognition (bool): Initial speaker recognition setting.
        """
        self.root_window = root
        self.quality = quality  # Initialize quality setting
        self.recognition = recognition # Initialize recognition setting

    def open_settings_window(self, calculate_window_pos):
        """
        Opens a new window for settings configuration.

        Args:
            calculate_window_pos (function): A function to calculate the window position.
        """
        # Create a new Toplevel window for settings
        self.settings_window = tk.Toplevel(self.root_window)
        self.settings_window.transient(self.root_window) # Set the window as transient to the root window
        self.settings_window.grab_set() # Capture all events, preventing interaction with the main window
        self.settings_window.title("Settings")
        self.settings_window.geometry(calculate_window_pos(250, 350)) # Set the window geometry
        
        quality_options = ["100", "90", "80", "70", "60", "50", "40", "30", "20", "10"] # Available quality options

        # Quality Dropdown Label
        ttk.Label(self.settings_window, text="Quality:", bootstyle="info").pack(pady=5)
        # Quality Dropdown
        quality = ttk.StringVar(value=self.quality) # Create a StringVar to hold the quality value
        quality_menu = ttk.Combobox(self.settings_window, textvariable=quality, values=quality_options, bootstyle="default") # Create a Combobox for quality selection
        quality_menu.pack()

        # Speaker Recognition Label
        ttk.Label(self.settings_window, text="Speaker Recognition:", bootstyle="info").pack(pady=5)
        # Speaker Recognition Switch
        recognition = tk.BooleanVar(value=self.recognition) # Create a BooleanVar to hold the recognition state
        switchButton = ttk.Checkbutton( # Create a Checkbutton acting as a switch
            self.settings_window,
            text="Enable Recognition",
            variable=recognition,
            bootstyle="switch"
        )
        switchButton.pack()

        # Button Frame
        button_frame = tk.Frame(self.settings_window)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        # Save Button
        save_button = ttk.Button(button_frame, text="Save", bootstyle="outline", command=lambda: self.save_settings(quality, recognition))
        save_button.pack(side=tk.RIGHT)

    def save_settings(self, quality, recognition):
        """
        Saves the selected settings and closes the settings window.

        Args:
            quality (ttk.StringVar): The selected quality value.
            recognition (tk.BooleanVar): The selected recognition state.
        """
        # Update the internal settings values
        self.quality = quality.get()
        self.recognition = recognition.get()
        # Destroy the settings window
        self.settings_window.destroy()