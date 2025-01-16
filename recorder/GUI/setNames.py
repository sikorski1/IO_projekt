import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
import os
import json
class SetNames:
    def __init__(self, root):
        self.root_window = root
        pass
    def open_set_name_window(self, calculate_window_pos):
        self.set_name_window = tk.Toplevel(self.root_window)
        self.set_name_window.title("Set Name")
        self.set_name_window.geometry(calculate_window_pos(350, 380))
        self.set_name_window.transient(self.root_window)
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
        try:
            with open(os.getcwd() + r"/recorder/speaker_registry.json", "w") as file:
                json.dump(updated_data, file, indent=4)
        except(FileNotFoundError, json.JSONDecodeError):
           messagebox.showinfo(FileNotFoundError, json.JSONDecodeError)
    
        messagebox.showinfo("Saved", "The names of the speakers have been saved")