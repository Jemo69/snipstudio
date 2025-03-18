import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sqlite3
import pyperclip
import os
import sys


class CodeStorageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SnipStudio")

        # Define themes
        self.themes = {
            "catppuccin": {
                "base": "#1e1e2e",
                "surface0": "#313244",
                "surface1": "#45475a",
                "text": "#89dceb",
                "subtext0": "#a6adc8",
                "accent_blue": "#89b4fa",
                "accent_purple": "#b4befe",
                "accent_mauve": "#cba6f7",
                "accent_orange": "#fab387",
                "accent_red": "#f38ba8",
                "accent_green": "#a6e3a1",
            },
            "dracula": {
                "base": "#282a36",
                "surface0": "#44475a",
                "surface1": "#6272a4",
                "text": "#f8f8f2",
                "subtext0": "#6272a4",
                "foreground": "#f8f8f2",
                "comment": "#6272a4",
                "selection": "#44475a",
                "currentLine": "#44475a",
                "accent_cyan": "#8be9fd",
                "accent_green": "#50fa7b",
                "accent_orange": "#ffb86c",
                "accent_pink": "#ff79c6",
                "accent_purple": "#bd93f9",
                "accent_red": "#ff5555",
                "accent_yellow": "#f1fa8c",
            },
            "one_dark": {
                "base": "#282c34",
                "surface0": "#3a3f4b",
                "surface1": "#5c6370",
                "text": "#abb2bf",
                "subtext0": "#5c6370",
                "foreground": "#abb2bf",
                "comment": "#5c6370",
                "selection": "#3e4451",
                "accent_green": "#98c379",
                "accent_orange": "#d19a66",
                "accent_purple": "#c678dd",
                "accent_keyword": "#c678dd",
                "accent_blue": "#61afef",
                "accent_yellow": "#e5c07b",
                "parameter": "#abb2bf",
                "operator": "#abb2bf",
                "punctuation": "#abb2bf",
                "accent_red": "#e06c75",
            },
            "tokyo_night": {
                "base": "#24283b",
                "surface0": "#2f3549",
                "surface1": "#414868",
                "text": "#c0caf5",
                "subtext0": "#565f89",
                "foreground": "#c8d3f5",
                "comment": "#565f89",
                "selection": "#3b4261",
                "accent_green": "#9ece6a",
                "accent_orange": "#ff9e64",
                "accent_purple": "#c6a0f6",
                "accent_keyword": "#bb9af7",
                "accent_blue": "#7aa2f7",
                "accent_yellow": "#e0af68",
                "parameter": "#c8d3f5",
                "operator": "#c8d3f5",
                "punctuation": "#c8d3f5",
                "accent_red": "#f7768e",
            },
            "night_owl": {
                "base": "#011627",
                "surface0": "#112630",
                "surface1": "#2d3f44",
                "subtext0": "#637777",
                "foreground": "#d6deeb",
                "comment": "#637777",
                "selection": "#1d3b53",
                "accent_green": "#addb67",
                "text": "#f78c6c",
                "accent_purple": "#c792ea",
                "accent_keyword": "#c792ea",
                "accent_blue": "#82aaff",
                "accent_yellow": "#ffcb8b",
                "parameter": "#d6deeb",
                "operator": "#c792ea",
                "punctuation": "#d6deeb",
                "accent_red": "#f07178",
            },
            "github_dark": {
                "base": "#0d1117",
                "surface0": "#161b22",
                "text": "#da3633",
                "surface1": "#8b949e",
                "accent_blue": "#58a6ff",
                "accent_blue_hover": "#1f6feb",
                "selection": "#30363d",
                "accent_green": "#238636",
                "accent_yellow": "#d29922",
                "accent_red": "#da3633",
                "accent_purple": "#8250df",
                "diff_add": "#28a745",
                "diff_remove": "#cb2431",
                "diff_change": "#e6b819",
                "code_background": "#161b22",
                "code_text": "#c9d1d9",
                "code_keyword": "#f97583",
                "code_string": "#9ecbff",
                "code_comment": "#6e7781",
                "code_number": "#79c0ff",
                "code_function": "#d2a8ff",
                "code_variable": "#c9d1d9",
                "code_operator": "#c9d1d9",
            },
            "moneygazer": {
                "base": "#060b13",
                "surface0": "#0c1527",
                "surface1": "#3e6ac1",
                "text": "#fc9d03",
                "subtext0": "#657b83",
                "foreground": "#eee8d5",
                "comment": "#93a1a1",
                "selection": "#002433",
                "accent_pink": "#d33682",
                "accent_blue": "#268bd2",
                "accent_green": "#859900",
                "accent_yellow": "#b58900",
                "accent_orange": "#cb4b16",
                "parameter": "#6c71c4",
                "operator": "#839496",
                "punctuation": "#93a1a1",
            },
        }

        # Set default theme
        self.current_theme = "catppuccin"
        # Initialize theme_var
        self.theme_var = tk.StringVar(value=self.current_theme)

        # Database setup
        self.conn = sqlite3.connect("code_snippets.db")
        self.create_table()
        self.create_settings_table()

        # Load last used theme and snippet
        self.load_last_used_theme()

        # Apply theme and configure UI
        self.configure_theme()
        self.set_title_bar()
        self.create_widgets()

        # Set application icon
        try:
            if getattr(sys, "frozen", False):
                application_path = sys._MEIPASS
            else:
                application_path = os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.join(application_path, "snipstudio.ico")
            self.root.iconbitmap(icon_path)
        except Exception:
            print("Icon not found, using default icon.")

        # Set application title with logo and apply theme

        self.root.geometry("1400x700")

        self.populate_listbox()
        self.populate_categories()
        self.load_last_used_snippet()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.bind("<Control-s>", lambda event: self.save_snippet())
        self.root.bind("<Control-h>", lambda event: self.show_keyboard_shortcuts())
        for i in range(10):
            self.root.bind(
                f"<Control-Key-{i}>",
                lambda event, index=i: self.go_to_snippet_by_index(index),
            )

    def set_title_bar(self):
        """Configures the title bar with the logo and title, applying the current theme."""
        theme_colors = self.themes[self.current_theme]
        title_frame = tk.Frame(self.root, bg=theme_colors["base"])
        title_frame.pack(fill=tk.X, padx=10, pady=5)

        try:
            if getattr(sys, "frozen", False):
                application_path = sys._MEIPASS
            else:
                application_path = os.path.dirname(os.path.abspath(__file__))
            logo_path = os.path.join(application_path, "snipstudio.jpg")
            self.logo_img = tk.PhotoImage(file=logo_path)
            self.logo_img = self.logo_img.subsample(30, 30)
            logo_label = tk.Label(
                title_frame, image=self.logo_img, bg=theme_colors["base"]
            )
            logo_label.pack(side=tk.LEFT, padx=(0, 10))
        except Exception:
            print("Logo image not found.")

        title_label = tk.Label(
            title_frame,
            text="SnipStudio",
            font=("Helvetica", 16, "bold"),
            fg=theme_colors["accent_blue"],
            bg=theme_colors["base"],
        )
        title_label.pack(side=tk.LEFT)

    def go_to_snippet_by_index(self, index):
        if self.listbox.size() > index:
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(index)
            self.listbox.see(index)
            self.show_snippet(None)

    def show_keyboard_shortcuts(self):
        theme_colors = self.themes[self.current_theme]
        shortcuts_window = tk.Toplevel(self.root)
        shortcuts_window.title("Keyboard Shortcuts")
        shortcuts_window.geometry("300x200")
        shortcuts_window.configure(bg=theme_colors["surface0"])

        shortcuts_text = scrolledtext.ScrolledText(
            shortcuts_window,
            wrap=tk.WORD,
            bg=theme_colors["surface0"],
            fg=theme_colors["text"],
            font=("Consolas", 10),
        )
        shortcuts_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        shortcuts = """
        Keyboard Shortcuts:
        - Ctrl+S: Save Snippet
        - Ctrl+K: Focus Search Bar
        - Ctrl+C: Copy Snippet
        - Ctrl+T: Clear Fields
        - Ctrl+0: Go to Snippet 1
        - Ctrl+1: Go to Snippet 2
        - Ctrl+2: Go to Snippet 3
        - Ctrl+3: Go to Snippet 4
        - Ctrl+4: Go to Snippet 5
        - Ctrl+5: Go to Snippet 6
        - Ctrl+6: Go to Snippet 7
        - Ctrl+7: Go to Snippet 8
        - Ctrl+8: Go to Snippet 9
        - Ctrl+9: Go to Snippet 10
        - Ctrl+H: Show this help
        """

        shortcuts_text.insert(tk.END, shortcuts)
        shortcuts_text.config(state=tk.DISABLED)

    def create_settings_table(self):
        cursor = self.conn.cursor()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS settings
                          (key TEXT PRIMARY KEY,
                           value TEXT)"""
        )
        self.conn.commit()

    def save_last_used_snippet(self, snippet_id):
        if snippet_id:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)",
                ("last_used_snippet", str(snippet_id)),
            )
            self.conn.commit()

    def load_last_used_snippet(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT value FROM settings WHERE key=?", ("last_used_snippet",))
        result = cursor.fetchone()

        if result:
            last_snippet_id = int(result[0])  # Ensure the ID is an integer
            cursor.execute("SELECT title FROM snippets WHERE id=?", (last_snippet_id,))
            title_result = cursor.fetchone()

            if title_result:
                title = title_result[0]
                for i in range(self.listbox.size()):
                    if self.listbox.get(i) == title:
                        self.listbox.selection_set(i)
                        self.listbox.see(i)
                        self.show_snippet_by_id(
                            last_snippet_id
                        )  # Use the dedicated method
                        break

    def show_snippet_by_id(self, snippet_id):
        """Show snippet details by ID, ensuring proper type handling."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM snippets WHERE id=?", (snippet_id,))
        row = cursor.fetchone()
        cursor.close()

        if row:
            self.title_var.set(row[1])
            self.category_var.set(row[2] if row[2] else "")
            self.code_editor.delete("1.0", tk.END)
            self.code_editor.insert("1.0", row[3])

    def on_closing(self):
        snippet_id = self.current_snippet_id()
        if snippet_id:
            self.save_last_used_snippet(snippet_id)

        self.save_last_used_theme(self.current_theme)

        if hasattr(self, "conn"):
            self.conn.close()

        self.root.destroy()

    def configure_theme(self):
        """Configures the application theme and applies it to the main window."""
        theme_colors = self.themes[self.current_theme]
        self.root.configure(bg=theme_colors["base"])

        style = ttk.Style()
        style.theme_create(
            "custom_theme",
            parent="alt",
            settings={
                "TFrame": {"configure": {"background": theme_colors["base"]}},
                "TLabel": {
                    "configure": {
                        "background": theme_colors["base"],
                        "foreground": theme_colors["text"],
                    }
                },
                "TButton": {
                    "configure": {
                        "background": theme_colors["surface1"],
                        "foreground": theme_colors["text"],
                        "padding": 6,
                        "relief": "flat",
                    },
                    "map": {
                        "background": [("active", theme_colors["base"])],
                        "foreground": [("active", theme_colors["surface1"])],
                    },
                },
                "TEntry": {
                    "configure": {
                        "foreground": theme_colors["text"],
                        "fieldbackground": theme_colors["surface0"],
                        "insertcolor": theme_colors["text"],
                        "borderwidth": 1,
                        "relief": "solid",
                    }
                },
                "TCombobox": {
                    "configure": {
                        "foreground": theme_colors["text"],
                        "fieldbackground": theme_colors["surface0"],
                        "selectbackground": theme_colors["accent_blue"],
                        "selectforeground": theme_colors["base"],
                    }
                },
            },
        )
        style.theme_use("custom_theme")

        self.root.option_add("*TCombobox*Listbox.background", theme_colors["surface0"])
        self.root.option_add("*TCombobox*Listbox.foreground", theme_colors["text"])
        self.root.option_add(
            "*TCombobox*Listbox.selectBackground", theme_colors["accent_blue"]
        )
        self.root.option_add(
            "*TCombobox*Listbox.selectForeground", theme_colors["base"]
        )

    def switch_theme(self, theme_name):
        """Switches the application theme and updates all widgets."""
        if theme_name in self.themes:
            self.current_theme = theme_name
            self.configure_theme()  # Re-configure the base theme settings
            self.refresh_ui_with_theme()  # Then refresh all UI elements
            self.save_last_used_theme(theme_name)

    def refresh_ui_with_theme(self):
        """Refreshes all UI components with the current theme colors."""
        theme_colors = self.themes[self.current_theme]

        # Update dynamic widgets
        self.listbox.config(
            bg=theme_colors["surface0"],
            fg=theme_colors["text"],
            selectbackground=theme_colors["accent_blue"],
            selectforeground=theme_colors["base"],
        )
        self.code_editor.config(
            bg=theme_colors["surface0"],
            fg=theme_colors["text"],
            insertbackground=theme_colors["text"],
            selectbackground=theme_colors["accent_blue"],
            selectforeground=theme_colors["base"],
        )

        # Update the title bar
        self.set_title_bar()

        # Since ttk widgets are already styled in configure_theme, we just need to refresh
        # any direct tk widgets or reapply styles if necessary.

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS snippets
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           title TEXT NOT NULL,
                           category TEXT,
                           code TEXT NOT NULL)"""
        )
        self.conn.commit()

    def focus_input(self, widget):
        widget.focus_set()

    def create_widgets(self):
        theme_colors = self.themes[self.current_theme]

        # Search Frame
        search_frame = ttk.Frame(self.root)
        search_frame.pack(pady=10, padx=10, fill=tk.X)

        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=(0, 5))
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        search_entry.bind("<KeyRelease>", self.search_snippets)
        self.root.bind("<Control-k>", lambda event: self.focus_input(search_entry))

        # Theme selection
        theme_frame = ttk.Frame(search_frame)
        theme_frame.pack(side=tk.RIGHT, padx=5)
        ttk.Label(theme_frame, text="Theme:").pack(side=tk.LEFT, padx=(0, 5))
        # Use the existing theme_var instead of creating a new one
        theme_combo = ttk.Combobox(
            theme_frame,
            textvariable=self.theme_var,
            values=list(self.themes.keys()),
            width=10,
        )
        theme_combo.pack(side=tk.LEFT)
        theme_combo.bind(
            "<<ComboboxSelected>>", lambda e: self.switch_theme(self.theme_var.get())
        )

        # Main Content Frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=20)

        # Listbox for snippets
        listbox_frame = ttk.Frame(main_frame)
        listbox_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        ttk.Label(listbox_frame, text="Snippets").pack(anchor=tk.W, pady=(0, 5))

        self.listbox = tk.Listbox(
            listbox_frame,
            width=25,
            bg=theme_colors["surface0"],
            fg=theme_colors["text"],
            selectbackground=theme_colors["accent_blue"],
            selectforeground=theme_colors["base"],
            borderwidth=1,
            highlightthickness=0,
        )
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.listbox.bind("<<ListboxSelect>>", self.show_snippet)

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

        # Code Editor
        ttk.Label(details_frame, text="Code:").pack(anchor=tk.W)
        self.code_editor = scrolledtext.ScrolledText(
            details_frame,
            wrap=tk.WORD,
            bg=theme_colors["surface0"],
            fg=theme_colors["text"],
            insertbackground=theme_colors["text"],
            selectbackground=theme_colors["accent_blue"],
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
        self.root.bind("<Control-t>", lambda event: self.clear_fields())

        delete_btn = ttk.Button(
            button_frame, text="Delete", command=self.delete_snippet
        )
        delete_btn.pack(side=tk.LEFT, padx=5)

        copy_btn = ttk.Button(button_frame, text="Copy", command=self.copy_snippet)
        copy_btn.pack(side=tk.LEFT, padx=5)
        self.root.bind("<Control-c>", lambda event: self.copy_snippet())

        shortcuts_btn = ttk.Button(
            button_frame, text="Shortcuts", command=self.show_keyboard_shortcuts
        )
        shortcuts_btn.pack(side=tk.RIGHT, padx=5)

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
        pyperclip.copy(self.code_editor.get("1.0", tk.END))
        messagebox.showinfo("Success", "Successfully Copied")

    def save_snippet(self):
        title = self.title_var.get().strip()
        category = self.category_var.get().strip()
        code = self.code_editor.get("1.0", tk.END).strip()
        if not title or not code:
            messagebox.showwarning("Input Error", "Title and Code are required!")
            return

        cursor = self.conn.cursor()
        if self.current_snippet_id():
            cursor.execute(
                """UPDATE snippets SET
                           title=?, category=?, code=?
                           WHERE id=?""",
                (title, category, code, self.current_snippet_id()),
            )
            message = "Snippet updated successfully"
        else:
            cursor.execute(
                """INSERT INTO snippets (title, category, code)
                           VALUES (?, ?, ?)""",
                (title, category, code),
            )
            cursor.execute("SELECT last_insert_rowid()")
            new_id = cursor.fetchone()[0]
            self.save_last_used_snippet(new_id)
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
            self.save_last_used_snippet(row[0])

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

    def save_last_used_theme(self, theme_name):
        if theme_name:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)",
                ("last_used_theme", theme_name),
            )
            self.conn.commit()

    def load_last_used_theme(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT value FROM settings WHERE key=?", ("last_used_theme",))
        result = cursor.fetchone()
        if result:
            last_theme_name = result[0]
            if last_theme_name in self.themes:
                self.current_theme = last_theme_name
                # Updated to use the theme_var that's now initialized earlier
                self.theme_var.set(last_theme_name)


if __name__ == "__main__":
    root = tk.Tk()
    app = CodeStorageApp(root)
    root.mainloop()
