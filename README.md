# SnipStudio - Code Snippet Manager

SnipStudio is a simple and user-friendly application for storing and managing code snippets. Built with Python and Tkinter, it provides a graphical interface to easily organize, search, and copy your code snippets.

## Features

- **Store Code Snippets:** Save code snippets with titles, categories, and the code itself.
- **Categorize Snippets:** Organize snippets by category for better management.
- **Search Functionality:** Quickly find snippets using keywords in titles, categories, or code content.
- **Syntax Highlighting (Planned):** Future versions may include syntax highlighting for better code readability.
- **Copy to Clipboard:** Easily copy code snippets to the clipboard with a single click.
- **User-friendly Interface:** Intuitive graphical interface built with Tkinter and a modern Catppuccin theme.
- **Persistent Storage:** Snippets are stored in a local SQLite database for persistent access.

## How to contribute 

1. **Prerequisites:**
    - Python 3.12 installed on your system.
    - No external libraries are required as Tkinter, sqlite3, and pyperclip are usually included with Python or easily installable via pip.

2. **Download:**
    - Download the `snipstudio.py` file.

3. **Run:**
    - Open a terminal or command prompt.
    - Navigate to the directory where you saved `snipstudio.py`.
    - Run the application using: `python snipstudio.py`

## Usage

1. **Running the Application:**
    - After installation, run `snipstudio.py` to launch the application.

2. **Interface Overview:**
    - **Left Panel (Snippets List):** Displays a list of saved snippets. You can select a snippet to view its details.
    - **Search Bar:** Located at the top, use it to search for snippets by title, category, or code content.
    - **Details Panel (Right Side):**
        - **Title Field:** Enter the title of your snippet.
        - **Category Dropdown:** Select or enter a category for your snippet.
        - **Code Editor:** A text area to write or paste your code snippet.
        - **Buttons:**
            - **Save:** Saves or updates the current snippet.
            - **Clear:** Clears the title, category, and code editor fields.
            - **Delete:** Deletes the currently selected snippet.
            - **Copy:** Copies the code from the editor to the clipboard.

3. **Adding a New Snippet:**
    - Click the "Clear" button to start with empty fields (optional).
    - Enter a title for your snippet in the "Title" field.
    - Choose a category from the dropdown or type a new category.
    - Paste or write your code in the "Code" editor.
    - Click the "Save" button to save the snippet.

4. **Editing a Snippet:**
    - Select a snippet from the list on the left.
    - The snippet's details will be loaded into the title, category, and code editor fields.
    - Modify the details as needed.
    - Click the "Save" button to update the snippet.

5. **Deleting a Snippet:**
    - Select a snippet from the list.
    - Click the "Delete" button.
    - Confirm the deletion when prompted.

6. **Searching Snippets:**
    - Type your search query in the search bar at the top.
    - The snippet list will be updated to show snippets matching your search terms in the title, category, or code.

7. **Copying Snippets:**
    - Select a snippet from the list.
    - Click the "Copy" button to copy the code to your clipboard.
## How to install
### Installation

SnipStudio is distributed as executable files for Windows, Linux, and macOS. You can download the latest release from the [Releases page](https://github.com/your-github-username/snipstudio/releases).

**Windows:**

1. **Download:** Download the `snipstudio.exe` file from the Releases page.
2. **Run:** Double-click `snipstudio.exe` to run the application.

**Linux/macOS:**

1. **Download:** Download the `snipstudio-linux` or `snipstudio-macos` file depending on your operating system from the Releases page.
2. **Make Executable:** Open a terminal and navigate to the directory where you downloaded the file. Run the appropriate command to make the file executable:
   ```bash
   chmod +x ./snipstudio-linux  # For Linux
   ```
   or
   ```bash
   chmod +x ./snipstudio-macos  # For macOS
   ```
3. **Run:** Execute the application by running:
   ```bash
   ./snipstudio-linux  # For Linux
   ```
   or
   ```bash
   ./snipstudio-macos  # For macOS
   ```

**Note:**

- SnipStudio is built with Python 3.12.
- The release includes `pyperclip` for clipboard functionality, ensuring copy-paste operations work seamlessly.
- Executable files are available in the release section of the GitHub repository.

## License

SnipStudio is released under the MIT License. See the [LICENSE.md](LICENSE.md) file for more details.

## Contributing

Contributions are welcome! If you have suggestions for improvements or find any bugs, please feel free to open an issue or submit a pull request on the project repository.

## Author

 Ifeanyichukwu Nwachukwu 
