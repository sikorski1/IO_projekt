import tkinter as tk
import ttkbootstrap as ttk
class Settings:
    def __init__(self, root, platform, max_files_size, quality, recognition):
        self.root_window = root
        self.platform = platform
        self.max_files_size = max_files_size
        self.quality = quality
        self.recognition = recognition
    def open_settings_window(self, calculate_window_pos):
        self.settings_window = tk.Toplevel(self.root_window)
        self.settings_window.transient(self.root_window)
        self.settings_window.grab_set()
        self.settings_window.title("Settings")
        self.settings_window.geometry(calculate_window_pos(250, 350))

        platforms = ["teams", "zoom", "meet"]
        max_files_size = ["0.1GB", "10GB", "5GB", "3GB"]
        quality_options = ["100", "90", "80", "70", "60", "50", "40", "30", "20", "10"]

        ttk.Label(self.settings_window, text="Platform:", bootstyle="info").pack(pady=5)
        platform = ttk.StringVar(value=self.platform)
        platforms_menu = ttk.Combobox(self.settings_window, textvariable=platform, values=platforms, bootstyle="default")
        platforms_menu.pack()

        # Max File Size Dropdown
        ttk.Label(self.settings_window, text="Max File Size:", bootstyle="info").pack(pady=5)
        max_file_size = ttk.StringVar(value=self.max_files_size)
        max_files_size_menu = ttk.Combobox(self.settings_window, textvariable=max_file_size, values=max_files_size, bootstyle="default")
        max_files_size_menu.pack()

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
        save_button = ttk.Button(button_frame, text="Save", bootstyle="outline", command=lambda:self.save_settings(platform, max_file_size, quality, recognition))
        save_button.pack(side=tk.RIGHT)
    def save_settings(self, platform, max_file_size, quality, recognition):
        self.platform = platform.get()
        self.max_files_size = max_file_size.get()
        self.quality = quality.get()
        self.recognition = recognition.get()
        print(f"Settings saved:")
        print(f"Platform: {self.platform}")
        print(f"Max File Size: {self.max_files_size}")
        print(f"Quality: {self.quality}")
        print(f"Speaker Recognition: {self.recognition}")
        tk.messagebox.showinfo("Settings", "Settings have been saved successfully!")
        self.settings_window.destroy()