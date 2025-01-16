import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk
from fpdf import FPDF
import os
from tkinterPdfViewer import tkinterPdfViewer as pdf
class More:
    def __init__(self, root):
        self.root_window = root
        self.file_txt_path = None
        self.file_pdf_path = None
    def open_more_window(self, calculate_window_pos):
        self.more_window = tk.Toplevel(self.root_window)
        self.more_window.title("More")
        self.more_window.geometry(calculate_window_pos(350, 350))
        self.more_window.transient(self.root_window)
        self.more_window.grab_set()

        ttk.Label(self.more_window, text="Txt to pdf coverter", font=("Arial", 12)).pack(pady=5)
        ttk.Label(self.more_window, text="Select .txt file:", font=("Arial", 10)).pack(pady=10)
        file_txt_path_button = tk.Button(self.more_window, text="Browse", command=self.select_txt_file, bg="blue", fg="white", width=15)
        file_txt_path_button.pack(padx=5)

        if self.file_txt_path != None and len(self.file_pdf_path) != 0:
        
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

        if self.file_pdf_path != None: 
            self.file_pdf_path_label = ttk.Label(self.more_window, text=f"Selected: {self.file_pdf_path}", bootstyle="success", font=("Arial", 8))
        else:
            self.file_pdf_path_label = ttk.Label(self.more_window, text="No file selected", bootstyle="danger", font=("Arial", 8))
        self.file_pdf_path_label.pack(pady=5)

        open_pdf_button = ttk.Button(self.more_window, text="Open", bootstyle="primary", command=lambda:self.open_pdf(calculate_window_pos))
        open_pdf_button.pack()

    def select_txt_file(self):
        try:
            self.file_txt_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
            if self.file_txt_path != None and self.file_txt_path != "":
                self.file_txt_path_label.config(text=f"Selected: {self.file_txt_path}", bootstyle="success")
            else:
                self.file_txt_path_label.config(text="No file selected", bootstyle="danger")
        except Exception as e:
            print(f"Error during file selection: {e}")
            messagebox.showerror("Error", f"An error occurred: {e}")
    def select_pdf_file(self):
        try:
            self.file_pdf_path = filedialog.askopenfilename(filetypes=[("Pdf Files", "*.pdf")])
            if self.file_pdf_path != None and self.file_pdf_path != "":
                self.file_pdf_path_label.config(text=f"Selected: {self.file_pdf_path}", bootstyle="success")
            else:
                self.file_pdf_path_label.config(text="No file selected", bootstyle="danger")
        except Exception as e:
            print(f"Error during file selection: {e}")
            messagebox.showerror("Error", f"An error occurred: {e}")
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
    def open_pdf(self, calculate_window_pos):
        if not self.file_pdf_path:
            tk.messagebox.showerror("Error", "No PDF file selected!")
            return

        if not os.path.exists(self.file_pdf_path):

            tk.messagebox.showerror("Error", "PDF file not found!")
            return
        self.pdf_window = tk.Toplevel(self.more_window)
        self.pdf_window.title("PDF Viewer")
        self.pdf_window.geometry(calculate_window_pos(600, 600))
    
        d = pdf.ShowPdf().pdf_view(self.pdf_window, pdf_location=self.file_pdf_path, width=100, height=100)
        d.pack(expand=True, fill="both")
        self.file_pdf_path = ""
        self.file_pdf_path_label.config(text="No file selected", bootstyle="danger")