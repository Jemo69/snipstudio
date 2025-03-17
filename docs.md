# Documentation for SnipStudio - Code Snippet Manager

This document provides detailed documentation for SnipStudio, a code snippet manager application built with Python and Tkinter. It covers everything from installation and usage to understanding the code structure and extending its functionality, specifically for developers looking to customize or contribute.

## Overview

SnipStudio is a user-friendly application designed to help you store, organize, and quickly access code snippets. It features a graphical interface built with Tkinter and is styled with a modern Catppuccin theme by default. SnipStudio allows you to categorize snippets, search through them, and easily copy code to your clipboard.  For developers, SnipStudio offers a clean and extensible codebase, making it easy to understand and modify.

## Features

- **Store Code Snippets:** Save code snippets with titles, categories, and the code content itself. Snippets are stored in a SQLite database for persistence.
- **Categorize Snippets:** Organize snippets by category for easy management and retrieval. Categories enhance organization and searchability.
- **Search Functionality:** Find snippets quickly by searching titles, categories, or code content.  Leverages SQLite's LIKE operator for flexible searching.
- **Copy to Clipboard:** Copy code snippets to your clipboard with a single click. Uses the `pyperclip` library for cross-platform clipboard access.
- **User-friendly Interface:** Intuitive graphical interface built with Tkinter, styled with themes. Designed for ease of use and customization.
- **Persistent Storage:** Snippets are saved in a local SQLite database (`code_snippets.db`). Ensures data persistence across application sessions.
- **Theme Customization:** Easily switch between different themes (Catppuccin, Dracula, One Dark Pro, Tokyo Night Storm, Night Owl) and add your own. Theme system is designed to be easily extensible by modifying color dictionaries.
- **Keyboard Shortcuts:** Use keyboard shortcuts for efficient searching and saving.  Tkinter's event binding system allows for easy addition of new shortcuts.
- **Last Used Snippet Memory:** Remembers and loads the last snippet you were working on when you restart the application.  Utilizes the `settings` table in the database to persist application state.

## Setting up for Development and Contribution

To contribute to SnipStudio or modify the application, you'll need to set up a development environment. This involves cloning the repository and installing the necessary dependencies.

### Prerequisites

- **Git:** Git is required for version control and cloning the repository. You can download it from [https://git-scm.com/](https://git-scm.com/).
- **Python 3.12:** SnipStudio is built using Python 3.12. Ensure you have Python 3.12 installed on your system. You can download it from [https://www.python.org/](https://www.python.org/).

### Cloning the Repository

You can clone the SnipStudio repository from GitHub using several methods:

#### Cloning with Git (HTTPS)

This is the most common method. Open your terminal and navigate to the directory where you want to clone the repository. Then, run the following command:

```bash
git clone https://github.com/Jemo69/snipstudio.git
cd snipstudio
```


#### Cloning with GitHub CLI (HTTPS)

If you have the GitHub CLI (`gh`) installed, you can use it to clone the repository.  This method can simplify authentication with GitHub.

```bash
gh repo clone Jemo69/snipstudio
cd snipstudio
```


#### Cloning with SSH

If you have set up SSH keys with your GitHub account, you can clone using SSH. This avoids having to enter your credentials every time.

```bash
git clone git@github.com:Jemo69/snipstudio.git
cd snipstudio
```


### Installing Dependencies

After cloning the repository, navigate into the `snipstudio` directory in your terminal. You need to install the required Python packages.  Run the following command:

```bash
python -m pip install pyperclip
```

This command installs the `pyperclip` library, which is used by SnipStudio for clipboard operations.

### Running from Source

To run SnipStudio from the source code, execute the following command from the `snipstudio` directory:

```bash
python snipstudio.py
```

This will start the SnipStudio application, allowing you to test your changes and contribute to the project.

## Usage

### Interface Overview

- **Snippets List (Left Panel):** Displays a list of your saved snippets. Click a snippet to view its details in the editor on the right. This list is dynamically updated based on search queries.
- **Search Bar (Top):**  Type keywords to search snippets by title, category, or code. Use `Ctrl+K` or `Cmd+K` to focus on the search bar for quick access.
- **Snippet Details (Right Side):** This area allows you to view and edit snippet content.
    - **Title Field:** Edit the snippet title.  The title is used to identify and search for snippets.
    - **Category Dropdown:** Select or type a category for the snippet. Categories help in organizing snippets logically.
    - **Code Editor:**  A `scrolledtext` widget for viewing and editing the code snippet. Supports syntax highlighting if you integrate a library like `Pygments` (not currently implemented in the base version).
    - **Action Buttons:** Buttons to perform actions on the current snippet.
        - **Save:** Saves new snippets or updates existing ones. Bound to the `Ctrl+S` shortcut for efficiency.
        - **Clear:** Clears title, category, and code fields, allowing you to start a new snippet.
        - **Delete:** Removes the selected snippet from the database. Prompts for confirmation to prevent accidental deletion.
        - **Copy:** Copies the code from the editor to the clipboard.

- **Theme Dropdown (Top Right):** Select from available themes to customize the application's appearance.  Themes are defined as color dictionaries in the code, making it easy to add or modify them.

### Basic Operations

1. **Adding a New Snippet:**
    - Click "Clear" or simply start typing in the "Title" field to begin creating a new snippet.
    - Enter a descriptive title and select or type a category to organize your snippet.
    - Paste or write your code in the "Code" editor.  Supports multi-line code snippets.
    - Click "Save" or press `Ctrl+S` to store the snippet in the database.

2. **Editing a Snippet:**
    - Select a snippet from the list in the left panel. The snippet details will load into the right panel.
    - Modify the title, category, or code in the respective fields.
    - Click "Save" or press `Ctrl+S` to update the snippet in the database.

3. **Deleting a Snippet:**
    - Select a snippet from the list.
    - Click "Delete". A confirmation dialog will appear.
    - Confirm the deletion to permanently remove the snippet.

4. **Searching for Snippets:**
    - Type your search term in the search bar at the top.
    - The snippet list updates dynamically to show snippets matching your search query in title, category, or code.

5. **Copying Code:**
    - Select a snippet from the list.
    - Click "Copy". The code from the editor is copied to your clipboard, ready to be pasted elsewhere.

6. **Switching Themes:**
    - Use the theme dropdown in the top right corner to select a different theme.
    - The application's color scheme will change instantly to reflect the selected theme.

## Code Structure and Customization

SnipStudio's core logic is contained within the `snipstudio.py` file. The application is built around the `CodeStorageApp` class, which encapsulates all GUI elements and application logic.

### `CodeStorageApp` Class Breakdown

The `CodeStorageApp` class is the heart of SnipStudio. Here's a breakdown of its methods, focusing on developer-relevant details:

#### Initialization (`__init__(self, root)`)

- **Purpose:** Sets up the main application window and initializes all core components.
- **Functionality:**
    - Takes the main `Tk` window (`root`) as input.
    - Sets the window title to "SnipStudio".
    - Defines color palettes for various themes (Catppuccin, Dracula, One Dark Pro, Tokyo Night Storm, Night Owl) as dictionaries. These dictionaries are the basis for theme customization.
    - Attempts to load and set the application icon from `snipstudio.jpg`. Handles potential `FileNotFoundError` gracefully.
    - Creates the title bar frame and adds the logo and application name labels.
    - Sets the initial window size to 1400x700 pixels.
    - Calls `configure_theme()` to apply the default Catppuccin theme on startup.
    - Establishes a connection to the SQLite database `code_snippets.db`.
    - Calls `create_table()` and `create_settings_table()` to ensure the necessary database tables exist.
    - Calls `create_widgets()` to construct all GUI widgets (buttons, listboxes, text editors, etc.).
    - Calls `populate_listbox()` and `populate_categories()` to load data from the database into the GUI.
    - Calls `load_last_used_snippet()` to restore the last viewed snippet from the previous session.
    - Registers the `on_closing()` method to be executed when the window is closed, ensuring proper cleanup.
    - Binds the `Ctrl+S` keyboard shortcut to the `save_snippet()` method for quick saving.

#### Theme Configuration (`configure_theme(self)`)

- **Purpose:**  Applies the default Catppuccin theme to the application's UI.
- **Functionality:**
    - Sets the main window's background color using the `catppuccin` color palette.
    - Creates a `ttk.Style` object to manage widget styling.
    - Defines a custom Tkinter theme named "catppuccin" based on the `self.catppuccin` color dictionary. This theme specifies colors for various widget states (normal, active, etc.).
    - Configures styles for common `ttk` widgets like `TFrame`, `TLabel`, `TButton`, `TEntry`, and `TCombobox` to use colors from the Catppuccin palette.
    - Sets "catppuccin" as the currently active theme using `style.theme_use()`.
    - Initializes `self.themes` dictionary, which holds all available theme color palettes. This dictionary is crucial for theme switching and extension.
    - Configures the dropdown listbox style of `TCombobox` widgets to match the current theme's colors, ensuring visual consistency.

#### Theme Switching (`switch_theme(self, theme_name)`)

- **Purpose:**  Changes the application's theme to the theme specified by `theme_name`.
- **Functionality:**
    - Takes `theme_name` (string) as input, representing the desired theme.
    - Checks if `theme_name` is a valid key in the `self.themes` dictionary.
    - If valid:
        - Updates `self.current_theme` to the new `theme_name`.
        - Retrieves the corresponding color palette from `self.themes`.
        - Updates the main window's background color.
        - Reconfigures the `TCombobox` dropdown listbox styles.
        - Calls `refresh_ui_with_theme()` to update the colors of other themed widgets (like Listbox and Code Editor).

#### UI Refresh with Theme (`refresh_ui_with_theme(self)`)

- **Purpose:** Updates the colors of specific UI widgets when the theme is changed.
- **Functionality:**
    - Retrieves the color palette of the `self.current_theme`.
    - Updates the `background`, `foreground`, `selectbackground`, and `selectforeground` options of the `self.listbox` and `self.code_editor` widgets to reflect the new theme's colors.
    - **Note for Developers:** For a more comprehensive theme refresh, you would need to extend this method to iterate through all themed widgets and update their styles dynamically.  Currently, only Listbox and Code Editor are explicitly refreshed.

#### Database Table Creation (`create_table(self)`, `create_settings_table(self)`)

- **Purpose:** Creates the `snippets` and `settings` tables in the SQLite database if they don't already exist.
- **Functionality:**
    - `create_table(self)`:
        - Executes SQL `CREATE TABLE IF NOT EXISTS snippets` to create the `snippets` table.
        - Table schema: `id` (INTEGER PRIMARY KEY AUTOINCREMENT), `title` (TEXT NOT NULL), `category` (TEXT), `code` (TEXT NOT NULL).
    - `create_settings_table(self)`:
        - Executes SQL `CREATE TABLE IF NOT EXISTS settings` to create the `settings` table.
        - Table schema: `key` (TEXT PRIMARY KEY), `value` (TEXT).  Used for storing application settings like the last used snippet.
    - Both methods commit the changes to the database connection (`self.conn.commit()`).

#### Last Used Snippet Management (`save_last_used_snippet(self, snippet_id)`, `load_last_used_snippet(self)`)

- **Purpose:** Manages saving and loading the last used snippet ID to persist user workflow across sessions.
- **Functionality:**
    - `save_last_used_snippet(self, snippet_id)`:
        - Takes `snippet_id` (integer or None) as input.
        - Uses SQL `INSERT OR REPLACE INTO settings` to store the `snippet_id` associated with the key "last_used_snippet" in the `settings` table.
    - `load_last_used_snippet(self)`:
        - Executes SQL `SELECT value FROM settings WHERE key=?` to retrieve the `last_used_snippet` ID from the `settings` table.
        - If a result is found:
            - Queries the `snippets` table to get the `title` of the snippet with the retrieved ID.
            - If the title is found in the listbox, selects that snippet in the listbox and calls `show_snippet_by_id()` to display its details.

#### Snippet Display by ID (`show_snippet_by_id(self, snippet_id)`)

- **Purpose:**  Retrieves and displays a snippet's details based on its ID.
- **Functionality:**
    - Takes `snippet_id` (integer) as input.
    - Executes SQL `SELECT * FROM snippets WHERE id=?` to fetch all columns for the snippet with the given ID.
    - If a snippet is found:
        - Sets the `title_var`, `category_var`, and populates the `code_editor` with the retrieved snippet data.

#### Window Closing Handler (`on_closing(self)`)

- **Purpose:**  Handles actions to be performed when the application window is closed.
- **Functionality:**
    - Called when the user closes the main window (e.g., by clicking the close button).
    - Calls `current_snippet_id()` to get the ID of the currently selected snippet.
    - If a snippet is selected, calls `save_last_used_snippet()` to save its ID as the last used snippet.
    - Closes the database connection using `self.conn.close()`.
    - Destroys the main window using `self.root.destroy()`, terminating the Tkinter application.

#### Widget Creation (`create_widgets(self)`)

- **Purpose:** Creates and configures all GUI widgets of the application.
- **Functionality:**
    - Creates frames to organize widgets: `search_frame`, `theme_frame`, `main_frame`, `listbox_frame`, `details_frame`, `form_frame`, `button_frame`.
    - **Search Frame:**
        - Creates a `ttk.Label` for "Search:".
        - Creates a `ttk.Entry` for the search bar, bound to `self.search_var` (StringVar).
        - Binds the `<KeyRelease>` event to `self.search_snippets` for live searching as the user types.
        - Binds `Ctrl+K` and `Cmd+K` to `lambda event: self.focus_input(search_entry)` to focus the search entry using keyboard shortcuts.
    - **Theme Selection Frame:**
        - Creates a `ttk.Label` for "Theme:".
        - Creates a `ttk.Combobox` (`theme_combo`) bound to `self.theme_var` (StringVar), populated with theme names from `self.themes.keys()`.
        - Binds the `<<ComboboxSelected>>` event to `lambda e: self.switch_theme(self.theme_var.get())` to switch themes when a theme is selected from the dropdown.
    - **Main Content Frame:**  Serves as a container for the listbox and details panels.
    - **Listbox Frame:**
        - Creates a `ttk.Label` for "Snippets".
        - Creates a `tk.Listbox` (`self.listbox`) to display snippet titles, styled according to the current theme.
        - Binds the `<<ListboxSelect>>` event to `self.show_snippet` to display snippet details when a snippet is selected in the list.
        - Creates a `ttk.Scrollbar` and attaches it to the `self.listbox` for vertical scrolling.
    - **Details Frame:**  Contains the form for editing snippet details and action buttons.
    - **Form Frame:**
        - Creates `ttk.Label` and `ttk.Entry` for "Title", bound to `self.title_var` (StringVar).
        - Creates `ttk.Label` and `ttk.Combobox` (`self.category_combo`) for "Category", bound to `self.category_var` (StringVar).
    - **Code Editor:**
        - Creates a `scrolledtext.ScrolledText` widget (`self.code_editor`) for editing code, styled according to the current theme.
    - **Button Frame:**
        - Creates `ttk.Button` widgets for "Save", "Clear", "Delete", and "Copy", each bound to their respective methods (`self.save_snippet`, `self.clear_fields`, `self.delete_snippet`, `self.copy_snippet`).

#### Snippet List Population (`populate_listbox(self, search_query=None)`)

- **Purpose:**  Populates the `self.listbox` with snippet titles from the database.
- **Functionality:**
    - Clears the existing content of `self.listbox`.
    - Establishes a database cursor.
    - If `search_query` is provided:
        - Executes an SQL `SELECT` query with `LIKE` clauses to fetch snippets whose `title`, `category`, or `code` match the `search_query`.
    - If `search_query` is None:
        - Executes a simple `SELECT` query to fetch all snippets, ordered by `title`.
    - Iterates through the fetched rows and inserts the `title` (second column of each row) into the `self.listbox`.
    - Closes the database cursor.

#### Category Population (`populate_categories(self)`)

- **Purpose:** Populates the category `Combobox` with distinct categories from the database.
- **Functionality:**
    - Establishes a database cursor.
    - Executes SQL `SELECT DISTINCT category FROM snippets` to fetch unique categories from the `snippets` table.
    - Extracts the category names from the fetched rows (excluding None values).
    - Updates the `values` option of `self.category_combo` with the list of categories, making them available in the dropdown.
    - Closes the database cursor.

#### Copy Snippet to Clipboard (`copy_snippet(self)`)

- **Purpose:** Copies the text from the `code_editor` to the system clipboard.
- **Functionality:**
    - Uses `pyperclip.copy(self.code_editor.get('1.0', tk.END))` to copy the entire content of the `self.code_editor` widget to the clipboard.  Relies on the `pyperclip` library.

#### Save Snippet (`save_snippet(self)`)

- **Purpose:** Saves or updates a snippet in the database.
- **Functionality:**
    - Retrieves the `title`, `category`, and `code` from the respective input fields (`self.title_var`, `self.category_var`, `self.code_editor`).
    - Performs basic validation: checks if `title` and `code` are not empty. Shows a warning message box if validation fails.
    - Establishes a database cursor.
    - Checks if `self.current_snippet_id()` returns a valid ID (meaning an existing snippet is being edited).
        - If yes (update): Executes an SQL `UPDATE snippets` query to modify the existing snippet with the new `title`, `category`, and `code`.
        - If no (insert): Executes an SQL `INSERT INTO snippets` query to create a new snippet with the provided data.
            - After insertion, retrieves the `last_insert_rowid()` to get the ID of the newly created snippet and calls `self.save_last_used_snippet()` to save it as the last used snippet.
    - Commits the changes to the database.
    - Calls `self.populate_listbox()` and `self.populate_categories()` to refresh the snippet list and category dropdown in the GUI.
    - Shows a success message box to inform the user.

#### Delete Snippet (`delete_snippet(self)`)

- **Purpose:** Deletes the currently selected snippet from the database.
- **Functionality:**
    - Checks if `self.current_snippet_id()` returns a valid ID (meaning a snippet is selected). Shows an info message box if no snippet is selected.
    - Shows a confirmation dialog (`messagebox.askyesno()`) to ask the user for confirmation before deleting.
    - If the user confirms:
        - Establishes a database cursor.
        - Executes SQL `DELETE FROM snippets WHERE id=?` to delete the snippet with the ID returned by `self.current_snippet_id()`.
        - Commits the changes to the database.
        - Calls `self.populate_listbox()` to refresh the snippet list.
        - Calls `self.clear_fields()` to clear the input fields in the details panel.
        - Shows a success message box.

#### Show Snippet Details (`show_snippet(self, event)`)

- **Purpose:** Displays the details of a selected snippet in the input fields.
- **Functionality:**
    - Called when a snippet is selected in the `self.listbox` (triggered by the `<<ListboxSelect>>` event).
    - Gets the current selection from `self.listbox`. Returns if no selection is made.
    - Establishes a database cursor.
    - Executes SQL `SELECT * FROM snippets WHERE title=?` to fetch all data for the snippet whose title matches the selected title in the listbox.
    - If a snippet is found:
        - Sets `self.title_var`, `self.category_var`, and populates `self.code_editor` with the retrieved snippet data.
        - Calls `self.save_last_used_snippet()` to save the ID of the displayed snippet as the last used snippet.
    - Closes the database cursor.

#### Get Current Snippet ID (`current_snippet_id(self)`)

- **Purpose:** Retrieves the ID of the currently selected snippet from the listbox.
- **Functionality:**
    - Gets the current selection from `self.listbox`. Returns `None` if no snippet is selected.
    - Establishes a database cursor.
    - Executes SQL `SELECT id FROM snippets WHERE title=?` to fetch the `id` of the snippet whose title matches the selected title in the listbox.
    - Returns the retrieved `id` if found, otherwise returns `None`.
    - Closes the database cursor.

#### Clear Input Fields (`clear_fields(self)`)

- **Purpose:** Clears the title, category, and code editor input fields and deselects any listbox selection.
- **Functionality:**
    - Sets `self.title_var`, `self.category_var` to empty strings.
    - Clears the content of `self.code_editor` using `delete("1.0", tk.END)`.
    - Clears any selection in `self.listbox` using `selection_clear(0, tk.END)`.

#### Search Snippets (`search_snippets(self, event)`)

- **Purpose:**  Initiates a snippet search based on the text in the search bar.
- **Functionality:**
    - Called when a key is released in the search entry (bound to `<KeyRelease>` event).
    - Retrieves the search query from `self.search_var.get()`.
    - Calls `self.populate_listbox(search_query)` to update the snippet listbox with snippets matching the search query.

#### Destructor (`__del__(self)`)

- **Purpose:** Ensures the database connection is closed when the `CodeStorageApp` object is destroyed.
- **Functionality:**
    - Called when the `CodeStorageApp` object is garbage collected.
    - Checks if `self` has an attribute `conn` (database connection).
    - If yes, closes the database connection using `self.conn.close()`.  This is important for releasing database resources.

### Adding a New Theme

To add a new theme to SnipStudio, you need to define a new color dictionary and integrate it into the application. Here's a step-by-step guide for developers:

1. **Define a Color Dictionary:**
   - Open the `snipstudio.py` file and locate the `__init__` method of the `CodeStorageApp` class.
   - Within the `__init__` method, you'll see existing theme dictionaries like `self.catppuccin`, `self.dracula_colors`, etc.
   - Create a new dictionary variable (e.g., `self.my_new_theme_colors`) and define the color codes for your new theme.
   - **Important Color Keys:** Ensure your dictionary includes the following keys, as they are used throughout the application's styling:
     - `"base"`:  The primary background color of the application.
     - `"surface0"`, `"surface1"`:  Surface colors for panels and widget backgrounds, providing visual hierarchy.
     - `"text"`:  The primary text color, ensuring readability against the background.
     - `"subtext0"`:  A secondary text color, often used for less important text.
     - `"foreground"`:  Generally the same as `"text"`, used for widget foregrounds.
     - `"comment"`:  Color for comments (though syntax highlighting is not yet implemented in the base version).
     - `"selection"`:  Background color for selected text or items.
     - `"currentLine"`: Color for the current line in the code editor (if implemented).
     - `"cyan"`, `"green"`, `"orange"`, `"pink"`, `"purple"`, `"red"`, `"yellow"`, `"blue"`, `"lavender"`, `"mauve"`, `"peach"`:  Accent colors used for highlights, buttons, and other UI elements.  Not all themes need to use all of these, but providing a consistent set makes customization easier.

   ```python
   self.my_new_theme_colors = {
       "base": "#f0f0f0",        # Example light base color (light gray)
       "surface0": "#e0e0e0",    # Slightly darker surface
       "surface1": "#d0d0d0",    # Even darker surface
       "text": "#333333",        # Dark text for light theme (dark gray)
       "subtext0": "#666666",    # Slightly lighter dark text
       "foreground": "#333333",
       "comment": "#888888",     # Gray comment color
       "selection": "#c0c0c0",   # Light gray selection color
       "currentLine": "#d0d0d0",
       "cyan": "#00ffff",       # Example accent colors
       "green": "#00ff00",
       "blue": "#0000ff",
       # ... define other colors as needed, using hex color codes
   }
   ```

2. **Add Theme to `self.themes` Dictionary:**
   - In the `__init__` method, locate the `self.themes` dictionary initialization.
   - Add your new theme dictionary to `self.themes` with a descriptive name as the key. This name will appear in the theme dropdown in the application.

   ```python
   self.themes = {
       'catppuccin': self.catppuccin,
       'dracula': self.dracula_colors,
       'one_dark': self.one_dark_pro_colors,
       'tokyo_night': self.tokyo_night_storm,
       'night_owl': self.night_owl_colors,
       'my_new_theme': self.my_new_theme_colors  # Add your new theme here
   }
   ```

3. **Test Your Theme:**
   - Run the `snipstudio.py` script.
   - In the SnipStudio application, open the theme dropdown in the top right corner.
   - Your new theme (e.g., "my_new_theme") should be listed in the dropdown.
   - Select your new theme to apply it.
   - **Debugging:** If your theme doesn't look as expected, inspect the color values in your theme dictionary.  Tkinter uses standard color names and hex color codes (e.g., `#RRGGBB`).  You may need to adjust the color values to achieve the desired visual appearance.  Check for typos in the color keys and values.

### Adding a Keyboard Shortcut

SnipStudio uses Tkinter's event binding mechanism to implement keyboard shortcuts. Here's how to add a new shortcut for developers:

1. **Choose a Function to Bind:**
   - Identify the method in the `CodeStorageApp` class that you want to trigger with a keyboard shortcut (e.g., `self.clear_fields()`, `self.save_snippet()`, or a new method you create).

2. **Determine the Event Sequence:**
   - Tkinter uses event sequences to represent key combinations. Common sequences include:
     - `"<Control-s>"`: Ctrl+S (Windows/Linux)
     - `"<Command-s>"`: Cmd+S (macOS)
     - `"<Control-Shift-c>"`: Ctrl+Shift+C
     - `"<Alt-n>"`: Alt+N
     - `"<F1>"`: F1 function key
     - `"<Return>"`: Enter key
     - `"<Escape>"`: Escape key
   - Refer to the Tkinter documentation or online resources for a comprehensive list of event sequences.

3. **Bind the Shortcut:**
   - In the `__init__` method of the `CodeStorageApp` class, after the GUI widgets are created (typically towards the end of `__init__`), use the `bind()` method of the widget to which you want to attach the shortcut.  Often, you'll bind shortcuts to the main `root` window (`self.root`) to make them application-wide.
   - The `bind()` method takes two main arguments:
     - The event sequence string (e.g., `'<Control-c>'`).
     - A callback function to be executed when the shortcut is pressed.  You'll often use a `lambda` function to call the desired method with `self` and any necessary event arguments.

   **Example: Adding Ctrl+C to clear fields (Windows/Linux and Cmd+C for macOS):**

   ```python
   # ... inside the __init__ method, after widget creation ...

   self.root.bind('<Control-c>', lambda event: self.clear_fields())  # Ctrl+C for Windows/Linux
   self.root.bind('<Command-c>', lambda event: self.clear_fields())  # Cmd+C for macOS
   ```

   - **Explanation:**
     - `self.root.bind(...)`:  Binds the shortcut to the main application window (`self.root`).
     - `'<Control-c>'` and `'<Command-c>'`:  Event sequences for Ctrl+C and Cmd+C respectively.
     - `lambda event: self.clear_fields()`: A `lambda` function that acts as the callback.
       - `lambda event:`: Defines an anonymous function that takes an `event` object as input (Tkinter automatically passes the event object to bound functions).
       - `self.clear_fields()`:  Calls the `clear_fields()` method of the `CodeStorageApp` instance (`self`).  The `event` argument is not used in this particular callback, but it's often useful in other shortcut handlers to get information about the event.

4. **Test Your Shortcut:**
   - Run the `snipstudio.py` script.
   - Press the keyboard shortcut you defined (e.g., Ctrl+C or Cmd+C).
   - Verify that the associated function is executed correctly (e.g., the input fields are cleared).
   - **Debugging:** If your shortcut doesn't work, double-check:
     - The event sequence string for typos and correctness.
     - That you've bound the shortcut to the correct widget (usually `self.root` for application-wide shortcuts).
     - That the callback function is correctly defined and calls the intended method.
     - Use print statements within the callback function to debug if it's being executed when you press the shortcut.

**Common Keyboard Shortcut Event Sequences (Examples):**

- `"<Control-s>"`: Ctrl+S (Save)
- `"<Control-k>"`: Ctrl+K (Focus Search)
- `"<Command-k>"`: Cmd+K (Focus Search on macOS)
- `"<Alt-n>"`: Alt+N (New Snippet - if you add such functionality)
- `"<F1>"`: F1 (Help - if you implement help functionality)
- `"<Return>"`: Enter key (Often used to trigger default actions in entries or dialogs)
- `"<Escape>"`: Escape key (Often used to close dialogs or cancel operations)

Refer to the official Tkinter documentation and online resources for a complete guide to event binding and event sequences for more advanced shortcut customization.

## How to Contribute

Contributions to SnipStudio are welcome! If you have suggestions, bug reports, or want to contribute code improvements or new features:

- **Open an Issue:** For bug reports or feature requests, open an issue on the project's GitHub repository.  This is the best way to report problems or suggest enhancements.
- **Submit a Pull Request:** If you want to contribute code directly (bug fixes, new features, theme additions, etc.), submit a pull request with your changes.  Please ensure your code adheres to good Python practices and includes comments and documentation where appropriate.

## License

SnipStudio is licensed under the MIT License. See the `LICENSE.md` file for details.  This permissive license allows for free use, modification, and distribution.

## Author

Created by Ifeanyichukwu Nwachukwu



