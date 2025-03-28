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
            "catppuccin_mocha": {  # Darkest
                "base": "#1e1e2e",
                "mantle": "#181825",
                "crust": "#11111b",
                "surface0": "#313244",
                "surface1": "#45475a",
                "surface2": "#585b70",
                "overlay0": "#6c7086",
                "overlay1": "#7f849c",
                "overlay2": "#9399b2",
                "text": "#cdd6f4",
                "subtext0": "#a6adc8",
                "subtext1": "#bac2de",
                "accent_rosewater": "#f5e0dc",
                "accent_flamingo": "#f2cdcd",
                "accent_pink": "#f5c2e7",
                "accent_mauve": "#cba6f7",
                "accent_red": "#f38ba8",
                "accent_maroon": "#eba0ac",
                "accent_peach": "#fab387",
                "accent_yellow": "#f9e2af",
                "accent_green": "#a6e3a1",
                "accent_teal": "#94e2d5",
                "accent_sky": "#89dceb",
                "accent_sapphire": "#74c7ec",
                "accent_blue": "#89b4fa",
                "accent_lavender": "#b4befe",
            },
            "catppuccin_macchiato": {  # Darker
                "base": "#24273a",
                "mantle": "#1e2030",
                "crust": "#181926",
                "surface0": "#363a4f",
                "surface1": "#494d64",
                "surface2": "#5b6078",
                "overlay0": "#6e738d",
                "overlay1": "#8087a2",
                "overlay2": "#939ab7",
                "text": "#cad3f5",
                "subtext0": "#a5adce",
                "subtext1": "#b8c0e0",
                "accent_rosewater": "#f4dbd6",
                "accent_flamingo": "#f0c6c6",
                "accent_pink": "#f5bde6",
                "accent_mauve": "#c6a0f6",
                "accent_red": "#ed8796",
                "accent_maroon": "#ee99a0",
                "accent_peach": "#f5a97f",
                "accent_yellow": "#eed49f",
                "accent_green": "#a6da95",
                "accent_teal": "#8bd5ca",
                "accent_sky": "#91d7e3",
                "accent_sapphire": "#7dc4e4",
                "accent_blue": "#8aadf4",
                "accent_lavender": "#b7bdf8",
            },
            "catppuccin_frappe": {  # Medium-Dark
                "base": "#303446",
                "mantle": "#292c3c",
                "crust": "#232634",
                "surface0": "#414559",
                "surface1": "#51576d",
                "surface2": "#626880",
                "overlay0": "#737994",
                "overlay1": "#838ba7",
                "overlay2": "#949cbb",
                "text": "#c6d0f5",
                "subtext0": "#a5adce",
                "subtext1": "#b5bfe2",
                "accent_rosewater": "#f2d5cf",
                "accent_flamingo": "#eebebe",
                "accent_pink": "#f4b8e4",
                "accent_mauve": "#ca9ee6",
                "accent_red": "#e78284",
                "accent_maroon": "#ea999c",
                "accent_peach": "#ef9f76",
                "accent_yellow": "#e5c890",
                "accent_green": "#a6d189",
                "accent_teal": "#81c8be",
                "accent_sky": "#99d1db",
                "accent_sapphire": "#85c1dc",
                "accent_blue": "#8caaee",
                "accent_lavender": "#babbf1",
            },
            "catppuccin_latte": {  # Light
                "base": "#eff1f5",
                "mantle": "#e6e9ef",
                "crust": "#dce0e8",
                "surface0": "#ccd0da",
                "surface1": "#bcc0cc",
                "surface2": "#acb0be",
                "overlay0": "#9ca0b0",
                "overlay1": "#8c8fa1",
                "overlay2": "#7c7f93",
                "text": "#4c4f69",
                "subtext0": "#6c6f85",
                "subtext1": "#5c5f77",
                "accent_rosewater": "#dc8a78",
                "accent_flamingo": "#dd7878",
                "accent_pink": "#ea76cb",
                "accent_mauve": "#8839ef",
                "accent_red": "#d20f39",
                "accent_maroon": "#e64553",
                "accent_peach": "#fe640b",
                "accent_yellow": "#df8e1d",
                "accent_green": "#40a02b",
                "accent_teal": "#179299",
                "accent_sky": "#04a5e5",
                "accent_sapphire": "#209fb5",
                "accent_blue": "#1e66f5",
                "accent_lavender": "#7287fd",
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
                "text": "#d6deeb",  # General text color
                "subtext0": "#637777",  # Less prominent text
                "foreground": "#d6deeb",  # Default foreground for code elements
                "comment": "#637777",
                "selection": "#1d3b53",
                "accent_green": "#addb67",  # Strings, etc.
                "accent_orange": "#f78c6c",  # Numbers, constants
                "accent_purple": "#c792ea",  # Keywords, special constants
                "accent_keyword": "#c792ea",  # Explicitly for keywords if needed
                "accent_blue": "#82aaff",  # Functions, classes
                "accent_yellow": "#ffcb8b",  # Variables, attributes
                "parameter": "#d6deeb",  # Function parameters
                "operator": "#c792ea",  # Operators
                "punctuation": "#d6deeb",  # Punctuation like brackets, commas
                "accent_red": "#f07178",  # Errors, important warnings
            },
            "gruvbox_dark": {
                "base": "#282828",
                "surface0": "#3c3836",
                "surface1": "#504945",
                "text": "#ebdbb2",
                "subtext0": "#a89984",
                "foreground": "#ebdbb2",
                "comment": "#928374",
                "selection": "#504945",
                "accent_green": "#b8bb26",
                "accent_orange": "#fe8019",
                "accent_purple": "#d3869b",
                "accent_keyword": "#fb4934",  # Often red in gruvbox
                "accent_blue": "#83a598",
                "accent_yellow": "#fabd2f",
                "parameter": "#ebdbb2",
                "operator": "#ebdbb2",
                "punctuation": "#ebdbb2",
                "accent_red": "#fb4934",
            },
            "solarized_dark": {
                "base": "#002b36",
                "surface0": "#073642",
                "surface1": "#586e75",
                "text": "#839496",
                "subtext0": "#586e75",
                "foreground": "#839496",
                "comment": "#586e75",
                "selection": "#073642",
                "accent_green": "#859900",
                "accent_orange": "#cb4b16",
                "accent_purple": "#d33682",
                "accent_keyword": "#cb4b16",  # Often orange
                "accent_blue": "#268bd2",
                "accent_yellow": "#b58900",
                "parameter": "#93a1a1",
                "operator": "#93a1a1",
                "punctuation": "#93a1a1",
                "accent_red": "#dc322f",
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

        # Set default theme (will be overridden by loaded theme if available)
        self.current_theme = "catppuccin"
        # Initialize theme_var
        self.theme_var = tk.StringVar(value=self.current_theme)

        # Database setup
        self.conn = sqlite3.connect("code_snippets.db")
        self.create_table()
        self.create_settings_table()

        # Load last used theme and snippet BEFORE creating widgets
        self.load_last_used_theme()
        # Set theme_var again after loading, in case it changed
        self.theme_var.set(self.current_theme)

        # Apply theme and configure UI
        self.configure_theme()  # Apply the loaded or default theme styling
        self.set_title_bar()
        self.create_widgets()  # Create widgets AFTER theme is known

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

        # Populate listbox and categories AFTER widgets are created
        self.populate_listbox()
        self.populate_categories()
        # Load last used snippet AFTER listbox is populated
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
        # Destroy existing title frame if it exists to prevent stacking
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame) and widget.winfo_name() == "!title_frame":
                widget.destroy()
                break

        theme_colors = self.themes[self.current_theme]
        title_frame = tk.Frame(self.root, bg=theme_colors["base"], name="!title_frame")
        # Pack it at the top, before other widgets
        title_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        try:
            if getattr(sys, "frozen", False):
                application_path = sys._MEIPASS
            else:
                application_path = os.path.dirname(os.path.abspath(__file__))
            logo_path = os.path.join(application_path, "snipstudio.jpg")
            # Ensure logo_img is stored as an instance attribute to prevent garbage collection
            self.logo_img = tk.PhotoImage(file=logo_path)
            self.logo_img = self.logo_img.subsample(30, 30)
            logo_label = tk.Label(
                title_frame, image=self.logo_img, bg=theme_colors["base"]
            )
            logo_label.pack(side=tk.LEFT, padx=(0, 10))
        except Exception as e:
            print(f"Logo image not found or error loading: {e}")

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
        shortcuts_window.geometry(
            "300x250"
        )  # Increased height to accommodate new shortcut
        shortcuts_window.configure(bg=theme_colors["surface0"])
        # Make the shortcuts window transient to the main window
        shortcuts_window.transient(self.root)
        shortcuts_window.grab_set()  # Keep focus

        shortcuts_text = scrolledtext.ScrolledText(
            shortcuts_window,
            wrap=tk.WORD,
            bg=theme_colors["surface0"],
            fg=theme_colors["text"],
            font=("Consolas", 10),
            bd=0,  # No border
            highlightthickness=0,  # No highlight border
        )
        shortcuts_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        shortcuts = """
        Keyboard Shortcuts:
        - Ctrl+S: Save Snippet
        - Ctrl+K: Focus Search Bar
        - Ctrl+C: Copy Snippet
        - Ctrl+T: Clear Fields
        - :<number>: Go to Snippet <number> (in listbox)
        - Ctrl+H: Show this help
        - Ctrl+<0-9>: Go to Snippet by index (0-9)
        - j/k: Move selection down/up (in listbox)
        """

        shortcuts_text.insert(tk.END, shortcuts.strip())
        shortcuts_text.config(state=tk.DISABLED)

        # Close window on Escape key
        shortcuts_window.bind("<Escape>", lambda e: shortcuts_window.destroy())
        # Ensure focus is set to the text widget initially if needed, though grab_set might handle it
        shortcuts_text.focus_set()

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
            try:
                cursor = self.conn.cursor()
                cursor.execute(
                    "INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)",
                    ("last_used_snippet", str(snippet_id)),
                )
                self.conn.commit()
            except sqlite3.Error as e:
                print(f"Database error saving last snippet: {e}")

    def load_last_used_snippet(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "SELECT value FROM settings WHERE key=?", ("last_used_snippet",)
            )
            result = cursor.fetchone()

            if result:
                try:
                    last_snippet_id = int(result[0])  # Ensure the ID is an integer
                    # Check if snippet ID exists before trying to select title
                    cursor.execute(
                        "SELECT title FROM snippets WHERE id=?", (last_snippet_id,)
                    )
                    title_result = cursor.fetchone()

                    if title_result:
                        title = title_result[0]
                        # Find the title in the listbox
                        listbox_items = self.listbox.get(0, tk.END)
                        if title in listbox_items:
                            index = listbox_items.index(title)
                            self.listbox.selection_set(index)
                            self.listbox.see(index)
                            self.show_snippet_by_id(
                                last_snippet_id
                            )  # Use the dedicated method
                        else:
                            print(
                                f"Last used snippet title '{title}' not found in listbox."
                            )
                    else:
                        print(
                            f"Last used snippet ID {last_snippet_id} not found in database."
                        )
                        # Optionally clear the setting if the snippet is gone
                        # cursor.execute("DELETE FROM settings WHERE key=?", ("last_used_snippet",))
                        # self.conn.commit()
                except ValueError:
                    print(
                        f"Invalid last used snippet ID found in settings: {result[0]}"
                    )
                except tk.TclError as e:
                    print(f"Error interacting with listbox during snippet load: {e}")
        except sqlite3.Error as e:
            print(f"Database error loading last snippet: {e}")

    def show_snippet_by_id(self, snippet_id):
        """Show snippet details by ID, ensuring proper type handling."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM snippets WHERE id=?", (snippet_id,))
            row = cursor.fetchone()
            cursor.close()  # Close cursor immediately after use

            if row:
                self.title_var.set(row[1])
                self.category_var.set(row[2] if row[2] else "")
                self.code_editor.delete("1.0", tk.END)
                self.code_editor.insert("1.0", row[3])
        except sqlite3.Error as e:
            print(f"Database error showing snippet by ID {snippet_id}: {e}")
        except tk.TclError as e:
            print(f"Error updating UI for snippet ID {snippet_id}: {e}")

    def on_closing(self):
        """Handles application closing cleanly."""
        snippet_id = self.current_snippet_id()
        if snippet_id:
            self.save_last_used_snippet(snippet_id)

        # Save the theme that was active when closing
        self.save_last_used_theme(self.current_theme)

        if hasattr(self, "conn"):
            try:
                self.conn.close()
            except sqlite3.Error as e:
                print(f"Error closing database on exit: {e}")

        self.root.destroy()

    def configure_theme(self):
        """Configures the application theme and applies it to the main window."""
        if self.current_theme not in self.themes:
            print(
                f"Warning: Theme '{self.current_theme}' not found. Falling back to default."
            )
            self.current_theme = "catppuccin"  # Fallback to a known theme

        theme_colors = self.themes[self.current_theme]
        self.root.configure(bg=theme_colors["base"])

        # Define or update the custom ttk theme
        style = ttk.Style()
        try:
            # Check if theme exists to avoid errors on re-configuration
            style.theme_use("custom_theme")
        except tk.TclError:
            # Create the theme if it doesn't exist
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
                            "borderwidth": 0,  # Ensure flat look
                            "font": ("Helvetica", 9),  # Consistent font
                        },
                        "map": {
                            # Use surface0 for hover, base for active press
                            "background": [
                                ("active", theme_colors["base"]),
                                ("hover", theme_colors["surface0"]),
                            ],
                            "foreground": [
                                ("active", theme_colors["text"])
                            ],  # Keep text color on press
                        },
                    },
                    "TEntry": {
                        "configure": {
                            "foreground": theme_colors["text"],
                            "fieldbackground": theme_colors["surface0"],
                            "insertcolor": theme_colors["text"],
                            "borderwidth": 1,  # Keep a subtle border
                            "relief": "flat",  # Use flat relief
                        },
                        "map": {
                            # Change border color on focus
                            "bordercolor": [("focus", theme_colors["accent_blue"])],
                            "relief": [
                                ("focus", "solid")
                            ],  # Make border visible on focus
                        },
                    },
                    "TCombobox": {
                        "configure": {
                            "foreground": theme_colors["text"],
                            "fieldbackground": theme_colors["surface0"],
                            "background": theme_colors[
                                "surface0"
                            ],  # Background of the entry part
                            "arrowcolor": theme_colors["text"],
                            "selectbackground": theme_colors[
                                "surface0"
                            ],  # Keep selection same as field bg
                            "selectforeground": theme_colors["text"],
                            "borderwidth": 1,
                            "relief": "flat",
                        },
                        "map": {
                            "background": [("readonly", theme_colors["surface0"])],
                            # Change border color on focus like TEntry
                            "bordercolor": [("focus", theme_colors["accent_blue"])],
                            "relief": [("focus", "solid")],
                        },
                    },
                    "Vertical.TScrollbar": {  # Style vertical scrollbars
                        "configure": {
                            "background": theme_colors["surface0"],
                            "troughcolor": theme_colors["base"],
                            "bordercolor": theme_colors["surface0"],
                            "arrowcolor": theme_colors["text"],
                            "relief": "flat",
                        },
                        "map": {"background": [("active", theme_colors["surface1"])]},
                    },
                },
            )
            style.theme_use("custom_theme")

        # Re-apply settings if theme already exists (useful if configure_theme is called again)
        style.configure("TFrame", background=theme_colors["base"])
        style.configure(
            "TLabel", background=theme_colors["base"], foreground=theme_colors["text"]
        )
        style.configure(
            "TButton",
            background=theme_colors["surface1"],
            foreground=theme_colors["text"],
        )
        style.map(
            "TButton",
            background=[
                ("active", theme_colors["base"]),
                ("hover", theme_colors["surface0"]),
            ],
        )
        style.configure(
            "TEntry",
            foreground=theme_colors["text"],
            fieldbackground=theme_colors["surface0"],
            insertcolor=theme_colors["text"],
        )
        style.map(
            "TEntry",
            bordercolor=[("focus", theme_colors["accent_blue"])],
            relief=[("focus", "solid")],
        )
        style.configure(
            "TCombobox",
            foreground=theme_colors["text"],
            fieldbackground=theme_colors["surface0"],
            background=theme_colors["surface0"],
            arrowcolor=theme_colors["text"],
        )
        style.map(
            "TCombobox",
            bordercolor=[("focus", theme_colors["accent_blue"])],
            relief=[("focus", "solid")],
        )
        style.configure(
            "Vertical.TScrollbar",
            background=theme_colors["surface0"],
            troughcolor=theme_colors["base"],
            bordercolor=theme_colors["surface0"],
            arrowcolor=theme_colors["text"],
        )
        style.map(
            "Vertical.TScrollbar", background=[("active", theme_colors["surface1"])]
        )

        # Configure Combobox dropdown list colors (using option_add for listbox part)
        # These need to be set before the Combobox is created ideally, but setting them here works too.
        self.root.option_add(
            "*TCombobox*Listbox.background", theme_colors["surface0"], priority=80
        )
        self.root.option_add(
            "*TCombobox*Listbox.foreground", theme_colors["text"], priority=80
        )
        self.root.option_add(
            "*TCombobox*Listbox.selectBackground",
            theme_colors["accent_blue"],
            priority=80,
        )
        self.root.option_add(
            "*TCombobox*Listbox.selectForeground", theme_colors["base"], priority=80
        )
        self.root.option_add(
            "*TCombobox*Listbox.font", ("Helvetica", 9), priority=80
        )  # Consistent font
        self.root.option_add("*TCombobox*Listbox.relief", "flat", priority=80)
        self.root.option_add("*TCombobox*Listbox.borderwidth", 0, priority=80)
        self.root.option_add("*TCombobox*Listbox.highlightthickness", 0, priority=80)

    def switch_theme(self, theme_name):
        """Saves the selected theme and restarts the application to apply it."""
        if theme_name in self.themes and theme_name != self.current_theme:
            if messagebox.askyesno(
                "Restart Required",
                "Changing the theme requires restarting the application. Restart now?",
            ):
                # Save the new theme choice
                self.save_last_used_theme(theme_name)

                # Perform necessary cleanup before restart
                snippet_id = self.current_snippet_id()
                if snippet_id:
                    self.save_last_used_snippet(snippet_id)
                if hasattr(self, "conn"):
                    try:
                        self.conn.close()
                    except sqlite3.Error as e:
                        print(
                            f"Error closing database before restart: {e}"
                        )  # Log error but continue

                # Restart the application
                try:
                    python = sys.executable
                    # Ensure sys.argv[0] is the script path, handle potential issues
                    script_path = os.path.abspath(sys.argv[0])
                    os.execv(python, [python, script_path] + sys.argv[1:])
                except Exception as e:
                    messagebox.showerror(
                        "Restart Error",
                        f"Failed to restart the application: {e}\nPlease restart manually.",
                    )
                    # Fallback: destroy the current window if restart fails
                    self.root.destroy()
            else:
                # User cancelled restart, revert the combobox selection back to the current theme
                self.theme_var.set(self.current_theme)
        elif theme_name == self.current_theme:
            # If the selected theme is already the current one, do nothing.
            pass
        else:
            # If theme_name is somehow invalid (shouldn't happen with Combobox)
            messagebox.showwarning("Theme Error", f"Theme '{theme_name}' not found.")
            self.theme_var.set(self.current_theme)  # Reset combobox

    # refresh_ui_with_theme is no longer needed as theme changes require restart
    # def refresh_ui_with_theme(self):
    #     ...

    def create_table(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS snippets
                              (id INTEGER PRIMARY KEY AUTOINCREMENT,
                               title TEXT NOT NULL,
                               category TEXT,
                               code TEXT NOT NULL)"""
            )
            # Add index for faster title lookups if it doesn't exist
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_snippet_title ON snippets (title)"
            )
            self.conn.commit()
        except sqlite3.Error as e:
            messagebox.showerror(
                "Database Error", f"Failed to create snippets table: {e}"
            )
            self.root.destroy()  # Exit if table creation fails

    def focus_input(self, widget):
        widget.focus_set()

    def create_widgets(self):
        theme_colors = self.themes[self.current_theme]

        # Main Content Frame (packed after title bar)
        main_frame = ttk.Frame(self.root, name="!main_frame")
        main_frame.pack(
            fill=tk.BOTH, expand=True, padx=10, pady=(0, 10)
        )  # Reduced bottom padding

        # --- Left Pane: Search, Theme, Listbox ---
        left_pane = ttk.Frame(main_frame, name="!left_pane")
        left_pane.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        # Search and Theme Frame (combined at the top of left pane)
        top_left_frame = ttk.Frame(left_pane, name="!top_left_frame")
        top_left_frame.pack(pady=(0, 10), fill=tk.X)  # Pad below this frame

        search_label = ttk.Label(top_left_frame, text="Search:")
        search_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 5))

        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(
            top_left_frame, textvariable=self.search_var, width=15
        )  # Adjust width as needed
        search_entry.grid(row=0, column=1, sticky=tk.EW, padx=(0, 10))
        search_entry.bind("<KeyRelease>", self.search_snippets)
        self.root.bind("<Control-k>", lambda event: self.focus_input(search_entry))

        theme_label = ttk.Label(top_left_frame, text="Theme:")
        theme_label.grid(row=0, column=2, sticky=tk.W, padx=(0, 5))

        theme_combo = ttk.Combobox(
            top_left_frame,
            textvariable=self.theme_var,
            values=list(self.themes.keys()),
            width=12,  # Adjust width
            state="readonly",  # Prevent typing custom themes
        )
        theme_combo.grid(row=0, column=3, sticky=tk.E)
        theme_combo.bind(
            "<<ComboboxSelected>>", lambda e: self.switch_theme(self.theme_var.get())
        )

        # Configure grid expansion for search entry
        top_left_frame.columnconfigure(1, weight=1)

        # Listbox Frame (below search/theme)
        listbox_frame = ttk.Frame(left_pane, name="!listbox_frame")
        listbox_frame.pack(
            fill=tk.BOTH, expand=True
        )  # Fill remaining space in left pane

        # Snippets Label removed, implied by the listbox

        self.listbox = tk.Listbox(
            listbox_frame,
            width=25,  # Keep width reasonable
            bg=theme_colors["surface0"],
            fg=theme_colors["text"],
            selectbackground=theme_colors["accent_blue"],
            selectforeground=theme_colors["base"],
            borderwidth=0,  # No border for the listbox itself
            highlightthickness=1,  # Use highlight for focus indication
            highlightcolor=theme_colors["accent_blue"],  # Color when focused
            highlightbackground=theme_colors["surface0"],  # Color when not focused
            relief="flat",
            exportselection=False,  # Prevent selection loss when focus moves
            font=("Helvetica", 10),
        )
        # Pack listbox first, then scrollbar
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        listbox_scrollbar = ttk.Scrollbar(
            listbox_frame,
            orient="vertical",
            command=self.listbox.yview,
            style="Vertical.TScrollbar",
        )
        listbox_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox.config(yscrollcommand=listbox_scrollbar.set)

        # Bindings for Listbox
        self.listbox.bind("<<ListboxSelect>>", self.show_snippet)
        self.listbox.bind(":", self.initiate_vim_command)  # Bind colon key
        self.listbox.bind(
            "<KeyPress-j>", self.move_selection_down
        )  # Use KeyPress for holding
        self.listbox.bind(
            "<KeyPress-k>", self.move_selection_up
        )  # Use KeyPress for holding
        self.listbox.bind("<Return>", self.show_snippet)  # Show snippet on Enter

        # --- Right Pane: Details ---
        details_frame = ttk.Frame(main_frame, name="!details_frame")
        details_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Title and Category Form Frame
        form_frame = ttk.Frame(details_frame, name="!form_frame")
        form_frame.pack(fill=tk.X, pady=(0, 10))  # Pad below form

        ttk.Label(form_frame, text="Title:").grid(
            row=0,
            column=0,
            sticky=tk.W,
            padx=(0, 5),
            pady=(0, 5),  # Reduced padding
        )
        self.title_var = tk.StringVar()
        title_entry = ttk.Entry(form_frame, textvariable=self.title_var)
        title_entry.grid(row=0, column=1, sticky=tk.EW, pady=(0, 5))

        ttk.Label(form_frame, text="Category:").grid(
            row=1, column=0, sticky=tk.W, padx=(0, 5), pady=(0, 5)
        )
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(form_frame, textvariable=self.category_var)
        # Populate values later in populate_categories
        self.category_combo.grid(row=1, column=1, sticky=tk.EW, pady=(0, 5))

        form_frame.columnconfigure(1, weight=1)  # Allow entry/combo to expand

        # Code Editor
        code_label = ttk.Label(details_frame, text="Code:")
        code_label.pack(anchor=tk.W, pady=(0, 2))  # Reduced padding

        self.code_editor = scrolledtext.ScrolledText(
            details_frame,
            wrap=tk.WORD,
            bg=theme_colors["surface0"],
            fg=theme_colors["text"],
            insertbackground=theme_colors["text"],  # Cursor color
            selectbackground=theme_colors["accent_blue"],
            selectforeground=theme_colors["base"],
            font=("Consolas", 10),
            borderwidth=0,  # No border for the text area
            highlightthickness=1,  # Use highlight for focus
            highlightcolor=theme_colors["accent_blue"],
            highlightbackground=theme_colors["surface0"],
            relief="flat",
            padx=5,  # Internal padding
            pady=5,
        )
        self.code_editor.pack(
            fill=tk.BOTH, expand=True, pady=(0, 10)
        )  # Pad below editor

        # Buttons Frame
        button_frame = ttk.Frame(details_frame, name="!button_frame")
        button_frame.pack(fill=tk.X)

        save_btn = ttk.Button(
            button_frame, text="Save (Ctrl+S)", command=self.save_snippet
        )
        save_btn.pack(side=tk.LEFT, padx=(0, 5))

        clear_btn = ttk.Button(
            button_frame, text="Clear (Ctrl+T)", command=self.clear_fields
        )
        clear_btn.pack(side=tk.LEFT, padx=5)
        self.root.bind("<Control-t>", lambda event: self.clear_fields())

        delete_btn = ttk.Button(
            button_frame, text="Delete", command=self.delete_snippet
        )
        delete_btn.pack(side=tk.LEFT, padx=5)

        copy_btn = ttk.Button(
            button_frame, text="Copy (Ctrl+C)", command=self.copy_snippet
        )
        copy_btn.pack(side=tk.LEFT, padx=5)
        self.root.bind("<Control-c>", lambda event: self.copy_snippet())

        # Move shortcuts button to the right
        shortcuts_btn = ttk.Button(
            button_frame,
            text="Shortcuts (Ctrl+H)",
            command=self.show_keyboard_shortcuts,
        )
        shortcuts_btn.pack(side=tk.RIGHT, padx=5)

        # Vim-like command entry (initially hidden, placed at bottom of main_frame)
        self.vim_command_entry = ttk.Entry(main_frame, name="!vim_command_entry")
        # Don't pack initially, use place or pack when needed
        self.vim_command_entry.bind("<Return>", self.process_vim_command)
        self.vim_command_entry.bind("<Escape>", self.hide_vim_command)
        self.vim_command_entry.bind("<FocusOut>", self.hide_vim_command)
        # Alt-v binding might conflict, consider changing or removing if problematic
        # self.root.bind("<Alt-v>", lambda event: self.focus_input(self.vim_command_entry))

    def initiate_vim_command(self, event):
        """Shows and focuses the Vim-like command entry at the bottom."""
        # Place the entry at the bottom of the main_frame
        self.vim_command_entry.place(relx=0, rely=1.0, relwidth=1.0, anchor=tk.SW)
        self.vim_command_entry.lift()  # Bring to front
        self.vim_command_entry.delete(0, tk.END)  # Clear previous command
        self.vim_command_entry.insert(0, ":")  # Start with colon
        self.vim_command_entry.icursor(tk.END)  # Move cursor to end
        self.vim_command_entry.focus_set()

    def move_selection_down(self, event):
        """Moves listbox selection down by one, wraps around."""
        current_selection = self.listbox.curselection()
        size = self.listbox.size()
        if not size:
            return  # Empty listbox

        current_index = current_selection[0] if current_selection else -1
        next_index = (current_index + 1) % size  # Wrap around

        self.listbox.selection_clear(0, tk.END)
        self.listbox.selection_set(next_index)
        self.listbox.see(next_index)
        self.show_snippet(None)  # Update details pane
        return "break"  # Prevent default listbox behavior if any

    def move_selection_up(self, event):
        """Moves listbox selection up by one, wraps around."""
        current_selection = self.listbox.curselection()
        size = self.listbox.size()
        if not size:
            return  # Empty listbox

        current_index = current_selection[0] if current_selection else 0
        prev_index = (current_index - 1 + size) % size  # Wrap around

        self.listbox.selection_clear(0, tk.END)
        self.listbox.selection_set(prev_index)
        self.listbox.see(prev_index)
        self.show_snippet(None)  # Update details pane
        return "break"  # Prevent default listbox behavior

    def process_vim_command(self, event):
        """Processes the command entered in the vim command entry."""
        command = self.vim_command_entry.get().strip()
        self.hide_vim_command(event)  # Hide entry after processing

        if command.startswith(":") and len(command) > 1:
            try:
                snippet_number = int(command[1:])
                self.go_to_snippet_by_number(snippet_number)
            except ValueError:
                messagebox.showerror(
                    "Command Error",
                    f"Invalid snippet number: '{command[1:]}'",
                    parent=self.root,
                )
            except Exception as e:
                messagebox.showerror(
                    "Command Error", f"Error processing command: {e}", parent=self.root
                )
        elif command == ":":  # Just colon entered
            pass  # Do nothing, just hide
        else:
            messagebox.showerror(
                "Command Error", f"Invalid command: '{command}'", parent=self.root
            )
        return "break"  # Prevent further processing

    def hide_vim_command(self, event=None):
        """Hides the Vim-like command entry."""
        self.vim_command_entry.place_forget()  # Remove from layout
        self.listbox.focus_set()  # Return focus to the listbox
        return "break"

    def go_to_snippet_by_number(self, number):
        """Navigates to the snippet by its 1-based listbox index."""
        index = number - 1  # 1-based to 0-based index
        if 0 <= index < self.listbox.size():
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(index)
            self.listbox.see(index)
            self.show_snippet(None)
        else:
            messagebox.showerror(
                "Navigation Error",
                f"Snippet number {number} out of range (1-{self.listbox.size()}).",
                parent=self.root,
            )

    def populate_listbox(self, search_query=None):
        """Populates the listbox with snippet titles, optionally filtered by search."""
        try:
            # Store current selection if any
            current_selection_index = self.listbox.curselection()
            selected_title = (
                self.listbox.get(current_selection_index[0])
                if current_selection_index
                else None
            )

            self.listbox.delete(0, tk.END)
            cursor = self.conn.cursor()
            query = "SELECT id, title FROM snippets"
            params = []

            if search_query:
                query += " WHERE title LIKE ? OR category LIKE ? OR code LIKE ?"
                like_query = f"%{search_query}%"
                params.extend([like_query, like_query, like_query])

            query += " ORDER BY title COLLATE NOCASE"  # Case-insensitive sorting

            cursor.execute(query, params)

            new_selection_index = -1
            count = 0
            for i, row in enumerate(cursor.fetchall()):
                self.listbox.insert(tk.END, row[1])
                if selected_title and row[1] == selected_title:
                    new_selection_index = i
                count += 1

            cursor.close()

            # Restore selection if the item still exists
            if new_selection_index != -1:
                self.listbox.selection_set(new_selection_index)
                self.listbox.see(new_selection_index)
            elif (
                count > 0 and not search_query
            ):  # If no search and previous selection gone, select first
                self.listbox.selection_set(0)
                self.listbox.see(0)
                self.show_snippet(None)  # Show the first item's details

        except sqlite3.Error as e:
            messagebox.showerror(
                "Database Error", f"Failed to populate snippets: {e}", parent=self.root
            )
        except tk.TclError as e:
            print(f"Error updating listbox: {e}")  # Log non-critical UI errors

    def populate_categories(self):
        """Populates the category combobox with distinct categories from the database."""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "SELECT DISTINCT category FROM snippets WHERE category IS NOT NULL AND category != '' ORDER BY category COLLATE NOCASE"
            )
            categories = [row[0] for row in cursor.fetchall()]
            self.category_combo["values"] = categories
            cursor.close()
        except sqlite3.Error as e:
            messagebox.showerror(
                "Database Error", f"Failed to load categories: {e}", parent=self.root
            )

    def copy_snippet(self):
        """Copies the content of the code editor to the clipboard."""
        try:
            code_content = self.code_editor.get("1.0", tk.END).strip()
            if code_content:
                pyperclip.copy(code_content)
                # Simple visual feedback might be better than a messagebox
                original_bg = self.copy_btn.cget("background")
                self.copy_btn.configure(text="Copied!")
                self.root.after(
                    1000, lambda: self.copy_btn.configure(text="Copy (Ctrl+C)")
                )
                # messagebox.showinfo("Success", "Snippet copied to clipboard.", parent=self.root)
            else:
                messagebox.showwarning(
                    "Copy Warning", "Nothing to copy.", parent=self.root
                )
        except pyperclip.PyperclipException as e:
            messagebox.showerror(
                "Clipboard Error", f"Could not copy to clipboard: {e}", parent=self.root
            )
        except tk.TclError as e:
            print(f"Error getting text from code editor: {e}")

    def save_snippet(self):
        """Saves the current snippet (new or update)."""
        title = self.title_var.get().strip()
        category = self.category_var.get().strip()
        code = self.code_editor.get("1.0", tk.END).strip()

        if not title or not code:
            messagebox.showwarning(
                "Input Error",
                "Title and Code fields cannot be empty.",
                parent=self.root,
            )
            return

        current_id = self.current_snippet_id()
        message = ""
        new_id = None

        try:
            cursor = self.conn.cursor()
            if current_id:
                # Update existing snippet
                cursor.execute(
                    """UPDATE snippets SET title=?, category=?, code=? WHERE id=?""",
                    (title, category, code, current_id),
                )
                message = f"Snippet '{title}' updated successfully."
                new_id = current_id  # Keep track of the ID
            else:
                # Insert new snippet
                cursor.execute(
                    """INSERT INTO snippets (title, category, code) VALUES (?, ?, ?)""",
                    (title, category, code),
                )
                new_id = cursor.lastrowid  # Get the ID of the newly inserted row
                message = f"Snippet '{title}' saved successfully."

            self.conn.commit()
            cursor.close()

            # Refresh UI
            self.populate_listbox(
                self.search_var.get()
            )  # Repopulate with current search
            self.populate_categories()

            # Reselect the saved/updated snippet in the listbox
            if new_id:
                cursor = self.conn.cursor()
                cursor.execute("SELECT title FROM snippets WHERE id=?", (new_id,))
                title_result = cursor.fetchone()
                cursor.close()
                if title_result:
                    new_title = title_result[0]
                    listbox_items = self.listbox.get(0, tk.END)
                    if new_title in listbox_items:
                        index = listbox_items.index(new_title)
                        self.listbox.selection_clear(0, tk.END)
                        self.listbox.selection_set(index)
                        self.listbox.see(index)
                        # Update last used snippet only if it's a new one or explicitly selected
                        self.save_last_used_snippet(new_id)

            # Show success feedback (optional, could use status bar later)
            # messagebox.showinfo("Success", message, parent=self.root)

        except sqlite3.Error as e:
            messagebox.showerror(
                "Database Error", f"Failed to save snippet: {e}", parent=self.root
            )
        except tk.TclError as e:
            print(f"Error getting text from editor during save: {e}")

    def delete_snippet(self):
        """Deletes the currently selected snippet."""
        snippet_id = self.current_snippet_id()
        if not snippet_id:
            messagebox.showinfo(
                "Info", "No snippet selected to delete.", parent=self.root
            )
            return

        # Get title for confirmation message
        selected_title = self.listbox.get(self.listbox.curselection()[0])

        if messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete the snippet '{selected_title}'?",
            parent=self.root,
        ):
            try:
                cursor = self.conn.cursor()
                cursor.execute("DELETE FROM snippets WHERE id=?", (snippet_id,))
                self.conn.commit()
                cursor.close()

                # Clear fields and refresh list
                self.clear_fields()  # Clear details first
                self.populate_listbox(
                    self.search_var.get()
                )  # Refresh list with current search
                self.populate_categories()  # Refresh categories

                # Optionally show success message
                # messagebox.showinfo("Success", f"Snippet '{selected_title}' deleted.", parent=self.root)

                # Check if the deleted snippet was the last used one and clear setting if so
                cursor = self.conn.cursor()
                cursor.execute(
                    "SELECT value FROM settings WHERE key=?", ("last_used_snippet",)
                )
                result = cursor.fetchone()
                if result and int(result[0]) == snippet_id:
                    cursor.execute(
                        "DELETE FROM settings WHERE key=?", ("last_used_snippet",)
                    )
                    self.conn.commit()
                cursor.close()

            except sqlite3.Error as e:
                messagebox.showerror(
                    "Database Error", f"Failed to delete snippet: {e}", parent=self.root
                )

    def show_snippet(self, event):
        """Displays the selected snippet's details in the editor."""
        selection = self.listbox.curselection()
        if not selection:
            # If nothing is selected (e.g., after delete/clear), ensure fields are clear
            # self.clear_fields() # Avoid clearing if selection lost focus temporarily
            return

        selected_title = self.listbox.get(selection[0])
        try:
            cursor = self.conn.cursor()
            # Fetch by title, assuming titles are unique enough for selection context
            cursor.execute("SELECT * FROM snippets WHERE title=?", (selected_title,))
            row = cursor.fetchone()
            cursor.close()

            if row:
                snippet_id = row[0]
                self.title_var.set(row[1])
                self.category_var.set(row[2] if row[2] else "")
                # Check if editor content is already the same to avoid unnecessary updates/flicker
                current_code = self.code_editor.get("1.0", tk.END).strip()
                new_code = row[3]
                if current_code != new_code:
                    self.code_editor.delete("1.0", tk.END)
                    self.code_editor.insert("1.0", new_code)
                # Save this as the last used snippet upon selection
                self.save_last_used_snippet(snippet_id)
            else:
                # Snippet title exists in listbox but not found in DB (should not happen with proper refresh)
                messagebox.showerror(
                    "Error",
                    f"Could not find details for snippet '{selected_title}'.",
                    parent=self.root,
                )
                self.populate_listbox(self.search_var.get())  # Refresh listbox

        except sqlite3.Error as e:
            messagebox.showerror(
                "Database Error",
                f"Failed to load snippet details: {e}",
                parent=self.root,
            )
        except tk.TclError as e:
            print(f"Error updating UI for snippet '{selected_title}': {e}")

    def current_snippet_id(self):
        """Gets the database ID of the currently selected snippet in the listbox."""
        selection = self.listbox.curselection()
        if not selection:
            return None

        selected_title = self.listbox.get(selection[0])
        try:
            cursor = self.conn.cursor()
            # Fetch ID based on the selected title
            cursor.execute("SELECT id FROM snippets WHERE title=?", (selected_title,))
            row = cursor.fetchone()
            cursor.close()
            return row[0] if row else None
        except sqlite3.Error as e:
            print(f"Database error getting current snippet ID: {e}")
            return None

    def clear_fields(self):
        """Clears the title, category, and code editor fields."""
        self.title_var.set("")
        self.category_var.set("")
        self.code_editor.delete("1.0", tk.END)
        self.listbox.selection_clear(0, tk.END)  # Deselect item in listbox
        # Optionally set focus to title or search
        # self.title_entry.focus_set() # Assuming self.title_entry exists

    def search_snippets(self, event):
        """Filters the listbox based on the search entry content."""
        search_query = self.search_var.get()
        self.populate_listbox(search_query)

    def __del__(self):
        """Ensures database connection is closed when the object is destroyed."""
        if hasattr(self, "conn") and self.conn:
            try:
                self.conn.close()
            except sqlite3.Error as e:
                # Might be called during interpreter shutdown, print might not work reliably
                # print(f"Error closing database in __del__: {e}")
                pass

    def save_last_used_theme(self, theme_name):
        """Saves the last used theme name and prompts user to restart."""
        if theme_name:
            try:
                cursor = self.conn.cursor()
                cursor.execute(
                    "INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)",
                    ("last_used_theme", theme_name),
                )
                self.conn.commit()
                cursor.close()
                # Inform user that a restart is required for the theme change
                messagebox.showinfo(
                    "Theme Changed",
                    f"Theme set to '{theme_name}'. Please restart the application for the change to take full effect.",
                    parent=self.root,
                )
            except sqlite3.Error as e:
                print(f"Database error saving last theme: {e}")
                messagebox.showerror(
                    "Database Error",
                    f"Failed to save theme setting: {e}",
                    parent=self.root,
                )

    def load_last_used_theme(self):
        """Loads the last used theme name from settings and sets it as current for startup."""
        # This function ensures the theme selected in the previous session is loaded when the app starts.
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "SELECT value FROM settings WHERE key=?", ("last_used_theme",)
            )
            result = cursor.fetchone()
            cursor.close()
            if result:
                last_theme_name = result[0]
                if last_theme_name in self.themes:
                    self.current_theme = last_theme_name
                    # The actual theme application happens during initialization using self.current_theme
                    # self.theme_var is updated in __init__ after this call
                else:
                    print(
                        f"Warning: Last used theme '{last_theme_name}' not found. Using default."
                    )
                    # Keep the default self.current_theme set in __init__
        except sqlite3.Error as e:
            print(f"Database error loading last theme: {e}")
            # Keep the default theme if loading fails


if __name__ == "__main__":
    root = tk.Tk()
    # Prevent the window from flashing before theme is applied
    root.withdraw()
    app = CodeStorageApp(root)
    # Make window visible after setup
    root.deiconify()
    root.mainloop()
