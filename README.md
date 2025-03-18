# SnipStudio - Code Snippet Manager

SnipStudio is designed to be a simple and easy-to-use application for anyone who wants to store and organize code snippets.  Whether you're just starting to code or are an experienced developer, SnipStudio helps you keep your code snippets handy. Built using Python and Tkinter, it has a friendly graphical interface to help you easily manage, search, and use your code snippets.

## Features

- **Store Code Snippets:**  Easily save pieces of code with titles, categories, and the code itself.
- **Categorize Snippets:** Organize your snippets by category to keep things tidy and easy to find.
- **Search Functionality:** Quickly find the snippets you need by searching for keywords in titles, categories, or the code content itself.
- **Copy to Clipboard:** Copy code snippets to your clipboard with a single click, making it super easy to paste them into your projects.
- **User-friendly Interface:**  SnipStudio has a clear and intuitive graphical interface, styled with a modern Catppuccin theme, so it's pleasant to use.
- **Persistent Storage:** Your snippets are saved in a local database, so they're always there when you need them.

## How to Install

SnipStudio is available as ready-to-run applications for Windows, Linux, and macOS. Here’s how to get it running:

### Installation

1. **Download:** Go to the [Releases page](https://github.com/your-github-username/snipstudio/releases) to download the latest version for your operating system.
    - For Windows, download the file ending in `.exe` (e.g., `snipstudio.exe`).
    - For Linux, download the file ending in `linux` (e.g., `snipstudio-linux`).
    - For macOS, download the file ending in `macos` (e.g., `snipstudio-macos`).

**Windows:**

1. **Run:** Once downloaded, simply double-click the `snipstudio.exe` file to start the application.

**Linux/macOS:**

1. **Make Executable (Linux/macOS only):** Open your computer's terminal program. Navigate to the folder where you downloaded the file. Then, make the file executable by typing the following command and pressing Enter:
   ```bash
   chmod +x ./snipstudio-linux  # For Linux
   ```
   or
   ```bash
   chmod +x ./snipstudio-macos  # For macOS
   ```
2. **Run:**  Now you can run the application by typing:
   ```bash
   ./snipstudio-linux  # For Linux
   ```
   or
   ```bash
   ./snipstudio-macos  # For macOS
   ```

**Note:**

- SnipStudio is built using Python 3.12. You don't need to have Python installed to run the downloaded application.
- It includes everything needed to copy and paste code snippets.
- You can always find the latest versions in the "Releases" section of the GitHub repository.

## Usage

Let's get started with using SnipStudio!

1. **Running the Application:**
    - After installing SnipStudio, run the application file you downloaded (`snipstudio.exe`, `snipstudio-linux`, or `snipstudio-macos`).

2. **Understanding the Interface:**
    SnipStudio's interface is straightforward:
    - **Snippets List (Left Panel):** This is where all your saved snippets are listed. Click on a snippet to see its details.
    - **Search Bar (Top):** Use this bar to type in keywords to find snippets quickly. SnipStudio will search through titles, categories, and code.
    - **Snippet Details (Right Side):** When you select a snippet, you'll see these fields:
        - **Title Field:**  Shows the title of the snippet. You can edit it here.
        - **Category Dropdown:**  Shows the category of the snippet. You can choose an existing category or type in a new one.
        - **Code Editor:** This is the large text area where the code of your snippet is displayed. You can write or paste code here.
        - **Action Buttons:** Below the code editor, you'll find buttons to:
            - **Save:**  Save changes or new snippets.
            - **Clear:**  Erase the current title, category, and code to start fresh.
            - **Delete:** Remove the currently selected snippet.
            - **Copy:** Copy the code from the editor to your computer's clipboard.

3. **Adding a New Snippet:**
    - To add a new snippet, you can click the "Clear" button to make sure the fields are empty (or just start typing!).
    - Type a title for your snippet in the "Title" field.
    - Choose a category from the "Category" dropdown, or type a new category name.
    - Enter or paste your code into the "Code" editor.
    - Click the "Save" button. Your snippet is now saved!

4. **Editing a Snippet:**
    - Select the snippet you want to change from the list on the left.
    - The snippet's information will appear in the "Title," "Category," and "Code" fields.
    - Make your changes in these fields.
    - Click "Save" to update the snippet with your edits.

5. **Deleting a Snippet:**
    - Choose the snippet you want to delete from the snippet list.
    - Click the "Delete" button.
    - SnipStudio will ask you to confirm if you really want to delete it. Click "OK" to delete.

6. **Searching for Snippets:**
    - Just type what you're looking for in the search bar at the top.
    - The list of snippets will automatically update to show only the snippets that match your search.

7. **Copying Code:**
    - Select the snippet you want to copy from the list.
    - Click the "Copy" button. The code is now copied to your clipboard, and you can paste it anywhere you need it!

## How to Contribute

Want to help make SnipStudio even better? Contributions are very welcome! If you have ideas for new features, find a bug, or want to improve the code, please feel free to:

- **Open an Issue:** If you find a bug or have a suggestion, open an issue on the project's repository to let us know.
- **Submit a Pull Request:** If you want to contribute code, submit a pull request with your changes.

## License

SnipStudio is open-source software licensed under the MIT License. Check out the [LICENSE.md](LICENSE.md) file for all the details.

## Author

 Created by Ifeanyichukwu Nwachukwu
