import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sqlite3
import pyperclip


class CodeStorageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SnipStudio")
        self.root.geometry("1400x700")

        # Catppuccin theme
        self.catppuccin = {
            "base": "#1e1e2e",  # Dark base
            "surface0": "#313244",  # Slightly lighter base
            "surface1": "#45475a",  # Even lighter base for contrast
            "text": "#cdd6f4",  # Main text color
            "subtext0": "#a6adc8",  # Secondary text color
            "blue": "#89b4fa",  # Highlight color
            "lavender": "#b4befe",  # Secondary highlight
            "mauve": "#cba6f7",  # Accent color
            "peach": "#fab387",  # Warning color
            "red": "#f38ba8",  # Error/Delete color
            "green": "#a6e3a1",  # Success color
        }

        self.dracula_colors = {
            "base": "#282a36",
            "surface0": "#44475a",
            "surface1": "#6272a4",
            "text": "#f8f8f2",
            "subtext0": "#6272a4",
            "foreground": "#f8f8f2",
            "comment": "#6272a4",
            "selection": "#44475a",
            "currentLine": "#44475a",
            "cyan": "#8be9fd",
            "green": "#50fa7b",
            "orange": "#ffb86c",
            "pink": "#ff79c6",
            "purple": "#bd93f9",
            "red": "#ff5555",
            "yellow": "#f1fa8c",
        }

        self.one_dark_pro_colors = {
            "base": "#282c34",
            "surface0": "#3a3f4b",
            "surface1": "#5c6370",
            "text": "#abb2bf",
            "subtext0": "#5c6370",
            "foreground": "#abb2bf",
            "comment": "#5c6370",
            "selection": "#3e4451",
            "string": "#98c379",
            "number": "#d19a66",
            "boolean": "#c678dd",
            "keyword": "#c678dd",
            "function": "#61afef",
            "class": "#e5c07b",
            "parameter": "#abb2bf",
            "operator": "#abb2bf",
            "punctuation": "#abb2bf",
            "variable": "#e06c75",
        }

        self.tokyo_night_storm = {
            "base": "#24283b",
            "surface0": "#2f3549",
            "surface1": "#414868",
            "text": "#c0caf5",
            "subtext0": "#565f89",
            "foreground": "#c8d3f5",
            "comment": "#565f89",
            "selection": "#3b4261",
            "string": "#9ece6a",
            "number": "#ff9e64",
            "boolean": "#c6a0f6",
            "keyword": "#bb9af7",
            "function": "#7aa2f7",
            "class": "#e0af68",
            "parameter": "#c8d3f5",
            "operator": "#c8d3f5",
            "punctuation": "#c8d3f5",
            "variable": "#f7768e",
        }

        self.night_owl_colors = {
            "base": "#011627",
            "surface0": "#112630",
            "surface1": "#2d3f44",
            "text": "#d6deeb",
            "subtext0": "#637777",
            "foreground": "#d6deeb",
            "comment": "#637777",
            "selection": "#1d3b53",
            "string": "#addb67",
            "text": "#f78c6c",
            "boolean": "#c792ea",
            "keyword": "#c792ea",
            "function": "#82aaff",
            "class": "#ffcb8b",
            "parameter": "#d6deeb",
            "operator": "#c792ea",
            "punctuation": "#d6deeb",
            "variable": "#f07178",
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
        self.root.configure(bg=self.catppuccin["base"])

        # Create a custom theme
        style = ttk.Style()
        style.theme_create(
            "catppuccin",
            parent="alt",
            settings={
                "TFrame": {"configure": {"background": self.catppuccin["base"]}},
                "TLabel": {
                    "configure": {
                        "background": self.catppuccin["base"],
                        "foreground": self.catppuccin["text"],
                    }
                },
                "TButton": {
                    "configure": {
                        "background": self.catppuccin["surface1"],
                        "foreground": self.catppuccin["text"],
                        "padding": 6,
                        "relief": "flat",
                    },
                    "map": {
                        "background": [("active", self.catppuccin["lavender"])],
                        "foreground": [("active", self.catppuccin["base"])],
                    },
                },
                "TEntry": {
                    "configure": {
                        "foreground": self.catppuccin["text"],
                        "fieldbackground": self.catppuccin["surface0"],
                        "insertcolor": self.catppuccin["text"],
                        "borderwidth": 1,
                        "relief": "solid",
                    }
                },
                "TCombobox": {
                    "configure": {
                        "foreground": self.catppuccin["text"],
                        "fieldbackground": self.catppuccin["surface0"],
                        "selectbackground": self.catppuccin["blue"],
                        "selectforeground": self.catppuccin["base"],
                    }
                },
            },
        )
        # Theme selection
        self.current_theme = 'catppuccin'  # Default theme
        self.themes = {
            'catppuccin': self.catppuccin,
            'dracula': self.dracula_colors,
            'one_dark': self.one_dark_pro_colors,
            'tokyo_night': self.tokyo_night_storm,
            'night_owl': self.night_owl_colors
        }
        
        style.theme_use(self.current_theme)

        # Configure combobox dropdown style based on current theme
        theme_colors = self.themes[self.current_theme]
        self.root.option_add("*TCombobox*Listbox.background", theme_colors["surface0"])
        self.root.option_add("*TCombobox*Listbox.foreground", theme_colors["text"])
        self.root.option_add("*TCombobox*Listbox.selectBackground", theme_colors["blue"])
        self.root.option_add("*TCombobox*Listbox.selectForeground", theme_colors["base"])

    def switch_theme(self, theme_name):
        if theme_name in self.themes:
            self.current_theme = theme_name
            theme_colors = self.themes[theme_name]
            
            # Update the UI with the new theme
            self.root.configure(bg=theme_colors["base"])
            
            # Update combobox styles
            self.root.option_add("*TCombobox*Listbox.background", theme_colors["surface0"])
            self.root.option_add("*TCombobox*Listbox.foreground", theme_colors["text"])
            self.root.option_add("*TCombobox*Listbox.selectBackground", theme_colors["blue"] if "blue" in theme_colors else theme_colors["selection"])
            self.root.option_add("*TCombobox*Listbox.selectForeground", theme_colors["base"])
            
            # Refresh widgets to apply new theme
            self.refresh_ui_with_theme()

    def refresh_ui_with_theme(self):
        # This method would update all widgets with the current theme
        # For a complete implementation, you would need to recreate or update all widgets
        theme_colors = self.themes[self.current_theme]
        
        # Update listbox colors
        self.listbox.config(
            bg=theme_colors["surface0"],
            fg=theme_colors["text"],
            selectbackground=theme_colors["blue"] if "blue" in theme_colors else theme_colors["selection"],
            selectforeground=theme_colors["base"]
        )
        
        # Update code editor colors
        self.code_editor.config(
            bg=theme_colors["surface0"],
            fg=theme_colors["text"],
            insertbackground=theme_colors["text"],
            selectbackground=theme_colors["blue"] if "blue" in theme_colors else theme_colors["selection"],
            selectforeground=theme_colors["base"]
        )

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

        # Theme selection
        theme_frame = ttk.Frame(search_frame)
        theme_frame.pack(side=tk.RIGHT, padx=5)
        ttk.Label(theme_frame, text="Theme:").pack(side=tk.LEFT, padx=(0, 5))
        self.theme_var = tk.StringVar(value=self.current_theme)
        theme_combo = ttk.Combobox(theme_frame, textvariable=self.theme_var, values=list(self.themes.keys()), width=10)
        theme_combo.pack(side=tk.LEFT)
        theme_combo.bind("<<ComboboxSelected>>", lambda e: self.switch_theme(self.theme_var.get()))

        # Main Content Frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=20)

        # Listbox for snippets with custom styling
        listbox_frame = ttk.Frame(main_frame)
        listbox_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        ttk.Label(listbox_frame, text="Snippets").pack(anchor=tk.W, pady=(0, 5))

        theme_colors = self.themes[self.current_theme]
        self.listbox = tk.Listbox(
            listbox_frame,
            width=25,
            bg=theme_colors["surface0"],
            fg=theme_colors["text"],
            selectbackground=theme_colors["blue"],
            selectforeground=theme_colors["base"],
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
            bg=theme_colors["surface0"],
            fg=theme_colors["text"],
            insertbackground=theme_colors["text"],
            selectbackground=theme_colors["blue"],
            selectforeground=theme_colors["base"],
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
