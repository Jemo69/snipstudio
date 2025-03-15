import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
import os

class CodeStorageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Code Storage App")

        self.code_entries = {}  # Dictionary to store code entries (filename: code)
        self.current_file = None # Tracks the currently open file

        # Menu Bar
        self.menu_bar = tk.Menu(root)
        root.config(menu=self.menu_bar)

        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(label="Save As...", command=self.save_file_as)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=root.quit)

        # Scrolled Text Area
        self.code_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, undo=True)
        self.code_text.pack(expand=True, fill=tk.BOTH)

    def new_file(self):
        self.code_text.delete(1.0, tk.END)
        self.current_file = None
        self.root.title("Code Storage App - New File")

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            try:
                with open(file_path, "r") as file:
                    code = file.read()
                    self.code_text.delete(1.0, tk.END)
                    self.code_text.insert(tk.END, code)
                    self.current_file = file_path
                    self.root.title(f"Code Storage App - {os.path.basename(file_path)}")

            except FileNotFoundError:
                messagebox.showerror("Error", "File not found.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

    def save_file(self):
        if self.current_file:
            try:
                with open(self.current_file, "w") as file:
                    file.write(self.code_text.get(1.0, tk.END))
                messagebox.showinfo("Saved", "File saved successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
        else:
            self.save_file_as()

    def save_file_as(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            try:
                with open(file_path, "w") as file:
                    file.write(self.code_text.get(1.0, tk.END))
                self.current_file = file_path
                self.root.title(f"Code Storage App - {os.path.basename(file_path)}")
                messagebox.showinfo("Saved", "File saved successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CodeStorageApp(root)
    root.mainloop()