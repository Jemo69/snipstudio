import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sqlite3
import pyperclip


class CodeStorageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SnipStudio")
        self.root.geometry("1400x700")

        # Catppuccin theme colors
        self.colors = {
            "base": "#1e1e2e",  # Dark background
            "surface0": "#313244",  # Slightly lighter background
            "surface1": "#45475a",  # Even lighter background for contrast
            "text": "#cdd6f4",  # Main text color
            "subtext0": "#a6adc8",  # Secondary text color
            "blue": "#89b4fa",  # Highlight color
            "lavender": "#b4befe",  # Secondary highlight
            "mauve": "#cba6f7",  # Accent color
            "peach": "#fab387",  # Warning color
            "red": "#f38ba8",  # Error/Delete color
            "green": "#a6e3a1",  # Success color
        }

        # Apply theme
        self.configure_theme()

        # Database setup
        self.conn = sqlite3.connect("code_snippets.db")
        self.create_table()

        # GUI Components
        self.create_widgets()
        self.populate_listbox()
        self.populate_categories()

    def configure_theme(self):
        # Configure the main window
        self.root.configure(bg=self.colors["base"])

        # Create a custom theme
        style = ttk.Style()
        style.theme_create(
            "catppuccin",
            parent="alt",
            settings={
                "TFrame": {"configure": {"background": self.colors["base"]}},
                "TLabel": {
                    "configure": {
                        "background": self.colors["base"],
                        "foreground": self.colors["text"],
                    }
                },
                "TButton": {
                    "configure": {
                        "background": self.colors["surface1"],
                        "foreground": self.colors["text"],
                        "padding": 6,
                        "relief": "flat",
                    },
                    "map": {
                        "background": [("active", self.colors["lavender"])],
                        "foreground": [("active", self.colors["base"])],
                    },
                },
                "TEntry": {
                    "configure": {
                        "foreground": self.colors["text"],
                        "fieldbackground": self.colors["surface0"],
                        "insertcolor": self.colors["text"],
                        "borderwidth": 1,
                        "relief": "solid",
                    }
                },
                "TCombobox": {
                    "configure": {
                        "foreground": self.colors["text"],
                        "fieldbackground": self.colors["surface0"],
                        "selectbackground": self.colors["blue"],
                        "selectforeground": self.colors["base"],
                    }
                },
            },
        )
        style.theme_use("catppuccin")

        # Configure combobox dropdown style
        self.root.option_add("*TCombobox*Listbox.background", self.colors["surface0"])
        self.root.option_add("*TCombobox*Listbox.foreground", self.colors["text"])
        self.root.option_add("*TCombobox*Listbox.selectBackground", self.colors["blue"])
        self.root.option_add("*TCombobox*Listbox.selectForeground", self.colors["base"])

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS snippets
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           title TEXT NOT NULL,
                           category TEXT,
                           code TEXT NOT NULL)""")
        self.conn.commit()

    def create_widgets(self):
        # Search Frame
        search_frame = ttk.Frame(self.root)
        search_frame.pack(pady=10, padx=10, fill=tk.X)

        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=(0, 5))
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        search_entry.bind("<KeyRelease>", self.search_snippets)

        # Main Content Frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=20)

        # Listbox for snippets with custom styling
        listbox_frame = ttk.Frame(main_frame)
        listbox_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        ttk.Label(listbox_frame, text="Snippets").pack(anchor=tk.W, pady=(0, 5))

        self.listbox = tk.Listbox(
            listbox_frame,
            width=25,
            bg=self.colors["surface0"],
            fg=self.colors["text"],
            selectbackground=self.colors["blue"],
            selectforeground=self.colors["base"],
            borderwidth=1,
            highlightthickness=0,
        )
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.listbox.bind("<<ListboxSelect>>", self.show_snippet)

        # Add scrollbar to listbox
        listbox_scrollbar = ttk.Scrollbar(
            listbox_frame, orient="vertical", command=self.listbox.yview
        )
        listbox_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=listbox_scrollbar.set)

        # Details Frame
        details_frame = ttk.Frame(main_frame)
        details_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Title and Category
        form_frame = ttk.Frame(details_frame)
        form_frame.pack(fill=tk.X, pady=(0, 20))

        ttk.Label(form_frame, text="Title:").grid(
            row=0, column=0, sticky=tk.W, padx=(0, 5), pady=10
        )
        self.title_var = tk.StringVar()
        title_entry = ttk.Entry(form_frame, textvariable=self.title_var)
        title_entry.grid(row=0, column=1, sticky=tk.EW, pady=10)

        ttk.Label(form_frame, text="Category:").grid(
            row=1, column=0, sticky=tk.W, padx=(0, 5), pady=10
        )
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(form_frame, textvariable=self.category_var)
        self.category_combo.grid(row=1, column=1, sticky=tk.EW, pady=5)

        form_frame.columnconfigure(1, weight=1)

        # Code Editor with custom styling
        ttk.Label(details_frame, text="Code:").pack(anchor=tk.W)
        self.code_editor = scrolledtext.ScrolledText(
            details_frame,
            wrap=tk.WORD,
            bg=self.colors["surface0"],
            fg=self.colors["text"],
            insertbackground=self.colors["text"],
            selectbackground=self.colors["blue"],
            selectforeground=self.colors["base"],
            font=("Consolas", 10),
        )
        self.code_editor.pack(fill=tk.BOTH, expand=True, pady=(5, 20))

        # Buttons
        button_frame = ttk.Frame(details_frame)
        button_frame.pack(fill=tk.X)

        save_btn = ttk.Button(button_frame, text="Save", command=self.save_snippet)
        save_btn.pack(side=tk.LEFT, padx=(0, 5))

        clear_btn = ttk.Button(button_frame, text="Clear", command=self.clear_fields)
        clear_btn.pack(side=tk.LEFT, padx=5)

        delete_btn = ttk.Button(
            button_frame, text="Delete", command=self.delete_snippet
        )
        delete_btn.pack(side=tk.LEFT, padx=5)
        copy_btn = ttk.Button(button_frame, text="Copy", command=self.copy_snippet)
        copy_btn.pack(side=tk.LEFT, padx=5)

    def populate_listbox(self, search_query=None):
        self.listbox.delete(0, tk.END)
        cursor = self.conn.cursor()

        if search_query:
            cursor.execute(
                """SELECT id, title FROM snippets 
                           WHERE title LIKE ? OR category LIKE ? OR code LIKE ?""",
                (f"%{search_query}%", f"%{search_query}%", f"%{search_query}%"),
            )
        else:
            cursor.execute("SELECT id, title FROM snippets ORDER BY title")

        for row in cursor.fetchall():
            self.listbox.insert(tk.END, row[1])
        cursor.close()

    def populate_categories(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT DISTINCT category FROM snippets")
        categories = [row[0] for row in cursor.fetchall() if row[0]]
        self.category_combo["values"] = categories
        cursor.close()

    def copy_snippet(self):
        pyperclip.copy(self.code_editor.get('1.0',tk.END))

    def save_snippet(self):
        title = self.title_var.get().strip()
        category = self.category_var.get().strip()
        code = self.code_editor.get("1.0", tk.END)
        if not title or not code.strip():
            messagebox.showwarning("Input Error", "Title and Code are required!")
            return

        cursor = self.conn.cursor()
        if self.current_snippet_id():
            # Update existing snippet
            cursor.execute(
                """UPDATE snippets SET 
                           title=?, category=?, code=?
                           WHERE id=?""",
                (title, category, code, self.current_snippet_id()),
            )
            message = "Snippet updated successfully"
        else:
            # Insert new snippet
            cursor.execute(
                """INSERT INTO snippets (title, category, code)
                           VALUES (?, ?, ?)""",
                (title, category, code),
            )
            message = "Snippet saved successfully"

        self.conn.commit()
        self.populate_listbox()
        self.populate_categories()
        messagebox.showinfo("Success", message)

    def delete_snippet(self):
        if not self.current_snippet_id():
            messagebox.showinfo("Info", "No snippet selected to delete")
            return

        if messagebox.askyesno(
            "Confirm Delete", "Are you sure you want to delete this snippet?"
        ):
            cursor = self.conn.cursor()
            cursor.execute(
                "DELETE FROM snippets WHERE id=?", (self.current_snippet_id(),)
            )
            self.conn.commit()
            self.populate_listbox()
            self.clear_fields()
            messagebox.showinfo("Success", "Snippet deleted successfully")

    def show_snippet(self, event):
        selection = self.listbox.curselection()
        if not selection:
            return

        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT * FROM snippets WHERE title=?", (self.listbox.get(selection[0]),)
        )
        row = cursor.fetchone()
        cursor.close()

        if row:
            self.title_var.set(row[1])
            self.category_var.set(row[2] if row[2] else "")
            self.code_editor.delete("1.0", tk.END)
            self.code_editor.insert("1.0", row[3])

    def current_snippet_id(self):
        selection = self.listbox.curselection()
        if not selection:
            return None

        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT id FROM snippets WHERE title=?", (self.listbox.get(selection[0]),)
        )
        row = cursor.fetchone()
        return row[0] if row else None

    def clear_fields(self):
        self.title_var.set("")
        self.category_var.set("")
        self.code_editor.delete("1.0", tk.END)
        self.listbox.selection_clear(0, tk.END)

    def search_snippets(self, event):
        search_query = self.search_var.get()
        self.populate_listbox(search_query)

    def __del__(self):
        if hasattr(self, "conn"):
            self.conn.close()


if __name__ == "__main__":
    root = tk.Tk()
    app = CodeStorageApp(root)
    root.mainloop()
