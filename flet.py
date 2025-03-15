import flet as ft
import sqlite3
import pyperclip


class CodeStorageApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Code Storage"
        self.page.window_width = 1600
        self.page.window_height = 900
        self.page.padding = 20
        
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

        # Database setup
        self.conn = sqlite3.connect("code_snippets.db")
        self.create_table()
        
        # Apply theme
        self.page.bgcolor = self.colors["base"]
        self.page.theme = ft.Theme(
            color_scheme=ft.ColorScheme(
                primary=self.colors["blue"],
                secondary=self.colors["lavender"],
                surface=self.colors["surface0"],
                background=self.colors["base"],
                on_primary=self.colors["base"],
                on_secondary=self.colors["base"],
                on_surface=self.colors["text"],
                on_background=self.colors["text"],
            )
        )
        
        # State variables
        self.current_id = None
        self.categories = []
        self.snippets = []
        
        # Create GUI components
        self.create_widgets()
        self.populate_categories()
        self.populate_snippets()
        
        # Add components to page
        self.build_layout()
        
    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS snippets
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           title TEXT NOT NULL,
                           category TEXT,
                           code TEXT NOT NULL)""")
        self.conn.commit()
    
    def create_widgets(self):
        # Search bar
        self.search_field = ft.TextField(
            label="Search",
            on_change=self.search_snippets,
            expand=True,
            border_color=self.colors["surface1"],
            focused_border_color=self.colors["blue"],
            color=self.colors["text"],
        )
        
        # Snippets list
        self.snippets_list = ft.ListView(
            spacing=2,
            padding=10,
            expand=True,
            auto_scroll=True
        )
        
        # Title and category
        self.title_field = ft.TextField(
            label="Title",
            border_color=self.colors["surface1"],
            focused_border_color=self.colors["blue"],
            color=self.colors["text"],
            expand=True
        )
        
        self.category_field = ft.Dropdown(
            label="Category",
            options=[],
            border_color=self.colors["surface1"],
            focused_border_color=self.colors["blue"],
            color=self.colors["text"],
            expand=True
        )
        
        # Code editor
        self.code_editor = ft.TextField(
            label="Code",
            multiline=True,
            min_lines=20,
            max_lines=30,
            border_color=self.colors["surface1"],
            focused_border_color=self.colors["blue"],
            color=self.colors["text"],
            text_style=ft.TextStyle(font_family="Monospace"),
            expand=True
        )
        
        # Action buttons
        self.save_button = ft.ElevatedButton(
            text="Save",
            on_click=self.save_snippet,
            bgcolor=self.colors["blue"],
            color=self.colors["base"]
        )
        
        self.clear_button = ft.ElevatedButton(
            text="Clear",
            on_click=self.clear_fields,
            bgcolor=self.colors["surface1"],
            color=self.colors["text"]
        )
        
        self.delete_button = ft.ElevatedButton(
            text="Delete",
            on_click=self.delete_snippet,
            bgcolor=self.colors["red"],
            color=self.colors["base"]
        )
        
        self.copy_button = ft.ElevatedButton(
            text="Copy",
            on_click=self.copy_snippet,
            bgcolor=self.colors["green"],
            color=self.colors["base"]
        )
    
    def build_layout(self):
        # Create layout
        search_row = ft.Row([
            ft.Text("Search:", color=self.colors["text"]),
            self.search_field
        ])
        
        snippets_container = ft.Container(
            content=ft.Column([
                ft.Text("Snippets", color=self.colors["text"]),
                self.snippets_list
            ]),
            padding=10,
            expand=1,
            bgcolor=self.colors["surface0"],
            border_radius=8
        )
        
        form_layout = ft.Column([
            ft.Row([
                ft.Text("Title:", width=80, color=self.colors["text"]),
                self.title_field
            ]),
            ft.Row([
                ft.Text("Category:", width=80, color=self.colors["text"]),
                self.category_field
            ]),
            ft.Container(height=10),
            ft.Text("Code:", color=self.colors["text"]),
            self.code_editor,
            ft.Container(height=20),
            ft.Row([
                self.save_button,
                self.clear_button,
                self.delete_button,
                self.copy_button
            ], spacing=10)
        ], expand=True)
        
        details_container = ft.Container(
            content=form_layout,
            padding=10,
            expand=3,
            bgcolor=self.colors["surface0"],
            border_radius=8
        )
        
        main_row = ft.Row(
            [snippets_container, details_container],
            spacing=10,
            expand=True
        )
        
        # Add all components to the page
        self.page.add(
            search_row,
            ft.Container(height=10),
            main_row
        )
    
    def populate_snippets(self, search_query=None):
        self.snippets_list.controls.clear()
        cursor = self.conn.cursor()
        
        if search_query:
            cursor.execute(
                """SELECT id, title FROM snippets 
                WHERE title LIKE ? OR category LIKE ? OR code LIKE ?""",
                (f"%{search_query}%", f"%{search_query}%", f"%{search_query}%"),
            )
        else:
            cursor.execute("SELECT id, title FROM snippets ORDER BY title")
        
        self.snippets = cursor.fetchall()
        
        for snippet_id, title in self.snippets:
            snippet_item = ft.TextButton(
                text=title,
                on_click=lambda e, id=snippet_id: self.show_snippet(id),
                style=ft.ButtonStyle(
                    color=self.colors["text"],
                    overlay_color=ft.colors.with_opacity(0.2, self.colors["blue"])
                ),
                width=float("inf"),
                alignment=ft.alignment.center_left
            )
            self.snippets_list.controls.append(snippet_item)
        
        self.page.update()
    
    def populate_categories(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT DISTINCT category FROM snippets")
        categories = [row[0] for row in cursor.fetchall() if row[0]]
        
        # Update dropdown options
        self.category_field.options = [
            ft.dropdown.Option(text=category) for category in categories
        ]
        self.categories = categories
        self.page.update()
    
    def show_snippet(self, snippet_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM snippets WHERE id=?", (snippet_id,))
        row = cursor.fetchone()
        
        if row:
            self.current_id = row[0]
            self.title_field.value = row[1]
            
            # Set category, handle if not in list
            if row[2] in self.categories:
                self.category_field.value = row[2]
            else:
                self.category_field.value = None
            
            self.code_editor.value = row[3]
            self.page.update()
    
    def save_snippet(self, e):
        title = self.title_field.value.strip() if self.title_field.value else ""
        category = self.category_field.value if self.category_field.value else ""
        code = self.code_editor.value if self.code_editor.value else ""
        
        if not title or not code.strip():
            self.show_message("Input Error", "Title and Code are required!")
            return
        
        cursor = self.conn.cursor()
        if self.current_id:
            # Update existing snippet
            cursor.execute(
                """UPDATE snippets SET 
                title=?, category=?, code=?
                WHERE id=?""",
                (title, category, code, self.current_id),
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
        self.populate_snippets()
        self.populate_categories()
        self.show_message("Success", message)
    
    def delete_snippet(self, e):
        if not self.current_id:
            self.show_message("Info", "No snippet selected to delete")
            return
        
        self.page.dialog = ft.AlertDialog(
            title=ft.Text("Confirm Delete"),
            content=ft.Text("Are you sure you want to delete this snippet?"),
            actions=[
                ft.TextButton("Yes", on_click=self.confirm_delete),
                ft.TextButton("No", on_click=self.close_dialog),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.dialog.open = True
        self.page.update()
    
    def confirm_delete(self, e):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM snippets WHERE id=?", (self.current_id,))
        self.conn.commit()
        self.populate_snippets()
        self.clear_fields(None)
        self.close_dialog(e)
        self.show_message("Success", "Snippet deleted successfully")
    
    def close_dialog(self, e):
        self.page.dialog.open = False
        self.page.update()
    
    def copy_snippet(self, e):
        if self.code_editor.value:
            pyperclip.copy(self.code_editor.value)
            self.show_message("Success", "Code copied to clipboard!")
        else:
            self.show_message("Info", "Nothing to copy")
    
    def clear_fields(self, e):
        self.current_id = None
        self.title_field.value = ""
        self.category_field.value = None
        self.code_editor.value = ""
        self.page.update()
    
    def search_snippets(self, e):
        search_query = self.search_field.value
        self.populate_snippets(search_query)
    
    def show_message(self, title, message):
        self.page.dialog = ft.AlertDialog(
            title=ft.Text(title),
            content=ft.Text(message),
            actions=[
                ft.TextButton("OK", on_click=self.close_dialog),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.dialog.open = True
        self.page.update()


def main(page: ft.Page):
    app = CodeStorageApp(page)


if __name__ == "__main__":
    ft.app(target=main)