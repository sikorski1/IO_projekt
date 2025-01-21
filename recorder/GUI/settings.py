import tkinter as tk
import ttkbootstrap as ttk

class Settings:
    def __init__(self, root, quality, recognition):
        self.root_window = root
        self.quality = quality
        self.recognition = recognition

    def open_settings_window(self, calculate_window_pos):
        self.settings_window = tk.Toplevel(self.root_window)
        self.settings_window.transient(self.root_window)
        self.settings_window.grab_set()
        self.settings_window.title("Settings")
        self.settings_window.geometry(calculate_window_pos(250, 350))

        quality_options = ["100", "90", "80", "70", "60", "50", "40", "30", "20", "10"]

        # Quality Dropdown
        ttk.Label(self.settings_window, text="Quality:", bootstyle="info").pack(pady=5)
        quality = ttk.StringVar(value=self.quality)
        quality_menu = ttk.Combobox(self.settings_window, textvariable=quality, values=quality_options, bootstyle="default")
        quality_menu.pack()

        ttk.Label(self.settings_window, text="Speaker Recognition:", bootstyle="info").pack(pady=5)
        recognition = tk.BooleanVar(value=self.recognition)
        switchButton = ttk.Checkbutton(
            self.settings_window,
            text="Enable Recognition",
            variable=recognition,
            bootstyle="switch"
        )
        switchButton.pack()

        button_frame = tk.Frame(self.settings_window)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        save_button = ttk.Button(button_frame, text="Save", bootstyle="outline", command=lambda: self.save_settings(quality, recognition))
        save_button.pack(side=tk.RIGHT)

    def save_settings(self, quality, recognition):
        self.quality = quality.get()
        self.recognition = recognition.get()
        self.settings_window.destroy()