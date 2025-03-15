import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext, Menu
import json
import os
import shutil
from datetime import datetime
from uuid import uuid4


class CodeStorageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Snip Studio ")
        self.root.geometry("1000x650")

        # Initialize data
        self.data_file = "code_snippets.json"
        self.backup_dir = "backups"
        self.snippets = self.load_snippets()
        self.current_snippet_id = None

        # Setup GUI
        self.setup_styles()
        self.create_main_layout()
        self.setup_menu()
        self.setup_autosave()
        self.update_tag_list()

    def setup_autosave(self):
        """Placeholder for autosave setup"""
        pass

    def update_tag_list(self):
        """Placeholder for updating tag list"""
        pass

    def filter_snippets(self, *args):
        """Placeholder for filtering snippets"""
        pass

    def populate_snippet_tree(self):
        """Placeholder for populating snippet tree"""
        pass

    def on_snippet_select(self, event):
        """Placeholder for snippet selection event"""
        pass

    def new_snippet(self):
        """Placeholder for new snippet action"""
        print("New snippet placeholder")

    def delete_snippet(self):
        """Placeholder for delete snippet action"""
        print("Delete snippet placeholder")

    def export_snippet(self):
        """Placeholder for export snippet action"""
        print("Export snippet placeholder")

    def import_snippet(self):
        """Placeholder for import snippet action"""
        print("Import snippet placeholder")

    def copy_to_clipboard(self):
        """Placeholder for copy to clipboard action"""
        print("Copy to clipboard placeholder")


    def setup_styles(self):
        # """Configure widget styles"""
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure(".", font=("Arial", 10))
        self.toggle_theme(initial=True)

    def toggle_theme(self, initial=False):
        """Toggle between light and dark themes"""
        if not hasattr(self, "is_dark_theme"):
            self.is_dark_theme = False

        if not initial:
            self.is_dark_theme = not self.is_dark_theme

        # Configure colors

        bg = "#2d2d2d" if self.is_dark_theme else "#f0f0f0"
        fg = "#ffffff" if self.is_dark_theme else "#000000"
        field_bg = "#3d3d3d" if self.is_dark_theme else "#ffffff"
        code_bg = "#1e1e1e" if self.is_dark_theme else "#ffffff"
        code_fg = "#dcdcdc" if self.is_dark_theme else "#000000"

        # Apply base styles
        self.style.configure(
            ".", background=bg, foreground=fg, fieldbackground=field_bg
        )
        self.root.configure(background=bg)

        # Configure code editor
        self.code_text.configure(bg=code_bg, fg=code_fg, insertbackground=fg)


        # Update all widgets
        self._update_widget_colors(self.root)

    def load_snippets(self):
        """Load snippets from JSON file with error handling"""
        try:
            # Create data file if it doesn't exist
            if not os.path.exists(self.data_file):
                with open(self.data_file, "w") as f:
                    json.dump({}, f)
                return {}

            # Load existing data
            with open(self.data_file, "r") as f:
                data = json.load(f)

                # Validate data structure
                if not isinstance(data, dict):
                    raise ValueError("Invalid data format")

                return data

        except (json.JSONDecodeError, ValueError) as e:
            messagebox.showerror(
                "Data Error", f"Corrupted data file: {str(e)}\nCreating new file."
            )
            with open(self.data_file, "w") as f:
                json.dump({}, f)
            return {}

        except Exception as e:
            messagebox.showerror("Loading Error", f"Failed to load snippets: {str(e)}")
            return {}


    def _update_widget_colors(self, widget):
        """Recursively update widget colors"""
        try:
            widget.configure(background=self.style.lookup(".", "background"))
            widget.configure(foreground=self.style.lookup(".", "foreground"))
        except:
            pass

        for child in widget.winfo_children():
            self._update_widget_colors(child)

    def create_main_layout(self):
        # Main container
        main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left frame for snippet list
        left_frame = ttk.Frame(main_paned, padding="5")
        main_paned.add(left_frame, weight=1)

        # Right frame for snippet editing
        right_frame = ttk.Frame(main_paned, padding="5")
        main_paned.add(right_frame, weight=2)

        # Setup frames
        self.setup_left_frame(left_frame)
        self.setup_right_frame(right_frame)

    def setup_menu(self):
        """Create menu bar"""
        menubar = Menu(self.root)
        self.root.config(menu=menubar)

        # File menu
        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label="Backup Now", command=self.create_backup)
        file_menu.add_command(label="Toggle Theme", command=self.toggle_theme)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)

    def setup_left_frame(self, parent):
        # Search and filter frame
        filter_frame = ttk.Frame(parent)
        filter_frame.pack(fill=tk.X, pady=(0, 5))

        # Search
        ttk.Label(filter_frame, text="Search:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(filter_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.search_var.trace("w", self.filter_snippets)

        # Tag filter
        ttk.Label(filter_frame, text="Tag:").pack(side=tk.LEFT, padx=(10, 0))
        self.tag_filter_var = tk.StringVar()
        self.tag_combobox = ttk.Combobox(filter_frame, textvariable=self.tag_filter_var)
        self.tag_combobox.pack(side=tk.LEFT, width=15)
        self.tag_filter_var.trace("w", self.filter_snippets)

        # Treeview for snippets
        tree_frame = ttk.Frame(parent)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("language", "date", "tags")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        self.tree.heading("language", text="Language")
        self.tree.heading("date", text="Date")
        self.tree.heading("tags", text="Tags")
        self.tree.column("language", width=100)
        self.tree.column("date", width=100)
        self.tree.column("tags", width=150)

        # Scrollbar
        tree_scroll = ttk.Scrollbar(
            tree_frame, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=tree_scroll.set)

        # Layout
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.bind("<<TreeviewSelect>>", self.on_snippet_select)

        # Buttons
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, pady=(5, 0))

        buttons = [
            ("New", self.new_snippet),
            ("Delete", self.delete_snippet),
            ("Export", self.export_snippet),
            ("Import", self.import_snippet),
        ]

        for text, cmd in buttons:
            ttk.Button(button_frame, text=text, command=cmd).pack(side=tk.LEFT, padx=2)

    def setup_right_frame(self, parent):
        # Details frame
        details_frame = ttk.Frame(parent)
        details_frame.pack(fill=tk.X, pady=(0, 5))

        # Title
        ttk.Label(details_frame, text="Title:").grid(row=0, column=0, sticky=tk.W)
        self.title_var = tk.StringVar()
        ttk.Entry(details_frame, textvariable=self.title_var).grid(
            row=0, column=1, sticky=tk.EW, padx=5
        )

        # Language
        ttk.Label(details_frame, text="Language:").grid(row=0, column=2, sticky=tk.W)
        self.language_var = tk.StringVar()
        languages = [
            "Python",
            "JavaScript",
            "HTML",
            "CSS",
            "Java",
            "C++",
            "C#",
            "PHP",
            "Ruby",
            "Go",
            "Rust",
            "Other",
        ]
        self.language_combo = ttk.Combobox(
            details_frame, textvariable=self.language_var, values=languages
        )
        self.language_combo.grid(row=0, column=3, sticky=tk.EW, padx=5)

        details_frame.columnconfigure(1, weight=1)
        details_frame.columnconfigure(3, weight=1)

        # Tags
        tags_frame = ttk.Frame(parent)
        tags_frame.pack(fill=tk.X, pady=(0, 5))

        ttk.Label(tags_frame, text="Tags:").pack(side=tk.LEFT)
        self.tags_var = tk.StringVar()
        ttk.Entry(tags_frame, textvariable=self.tags_var).pack(
            side=tk.LEFT, fill=tk.X, expand=True, padx=5
        )

        # Description
        desc_frame = ttk.Frame(parent)
        desc_frame.pack(fill=tk.X, pady=(0, 5))

        ttk.Label(desc_frame, text="Description:").pack(anchor=tk.W)
        self.description_text = scrolledtext.ScrolledText(desc_frame, height=3)
        self.description_text.pack(fill=tk.X, expand=True, padx=5)

        # Code editor
        code_frame = ttk.Frame(parent)
        code_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(code_frame, text="Code:").pack(anchor=tk.W)
        self.code_text = scrolledtext.ScrolledText(
            code_frame, wrap=tk.NONE, font=("Courier", 11), undo=True
        )
        self.code_text.pack(fill=tk.BOTH, expand=True, padx=5)

        # Horizontal scrollbar
        code_h_scroll = ttk.Scrollbar(
            code_frame, orient="horizontal", command=self.code_text.xview
        )
        self.code_text.configure(xscrollcommand=code_h_scroll.set)
        code_h_scroll.pack(fill=tk.X, padx=5)

        # Action buttons
        action_frame = ttk.Frame(parent)
        action_frame.pack(fill=tk.X)

        ttk.Button(action_frame, text="Save", command=self.save_snippet).pack(
            side=tk.RIGHT, padx=5
        )
        ttk.Button(action_frame, text="Copy", command=self.copy_to_clipboard).pack(
            side=tk.RIGHT, padx=5
        )

    # ... (Keep all other methods identical to the previous combined version)
    # Ensure all references to code editor use self.code_text

    def load_snippets(self):
        """Load snippets with error handling"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, "r") as f:
                    return json.load(f)
            return {}
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Corrupted data file! Creating new one.")
            return {}
        except Exception as e:
            messagebox.showerror("Error", f"Load failed: {str(e)}")
            return {}

    def save_snippets(self):
        """Save data with automatic backup"""
        try:
            with open(self.data_file, "w") as f:
                json.dump(self.snippets, f, indent=2)
            self.create_backup()
        except Exception as e:
            messagebox.showerror("Error", f"Save failed: {str(e)}")

    def create_backup(self):
        """Create timestamped backup"""
        try:
            os.makedirs(self.backup_dir, exist_ok=True)
            backup_file = os.path.join(
                self.backup_dir,
                f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            )
            shutil.copyfile(self.data_file, backup_file)
        except Exception as e:
            messagebox.showerror("Backup Failed", str(e))

    def save_snippet(self):
        """Save snippet with validation and version history"""
        title = self.title_var.get().strip()
        language = self.language_var.get()
        code = self.code_text.get("1.0", tk.END).strip()
        tags = self.tags_var.get().strip()

        # Validation
        if not title:
            messagebox.showerror("Error", "Title required")
            return
        if not code:
            messagebox.showerror("Error", "Code required")
            return
        if language and language not in self.language_combo["values"]:
            messagebox.showerror("Error", "Invalid language")
            return

        # Prepare snippet data
        snippet = {
            "title": title,
            "language": language,
            "tags": tags,
            "description": self.description_text.get("1.0", tk.END).strip(),
            "code": code,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "history": [],
        }

        # Add version history
        if self.current_snippet_id and self.current_snippet_id in self.snippets:
            existing = self.snippets[self.current_snippet_id]
            snippet["history"] = existing.get("history", [])[-4:]  # Keep last 5
            snippet["history"].append(
                {
                    "date": existing["date"],
                    "code": existing["code"],
                    "description": existing["description"],
                }
            )

        # Save to data
        if self.current_snippet_id:
            self.snippets[self.current_snippet_id] = snippet
        else:
            self.current_snippet_id = str(uuid4())
            self.snippets[self.current_snippet_id] = snippet

        # Update UI and data
        self.save_snippets()
        self.populate_snippet_tree()
        self.update_tag_list()
        self.tree.selection_set(self.current_snippet_id)
        self.tree.see(self.current_snippet_id)
        messagebox.showinfo("Saved", "Snippet saved successfully")

    # ... (Keep all other methods identical to previous version)


if __name__ == "__main__":
    root = tk.Tk()
    app = CodeStorageApp(root)
    root.mainloop()
