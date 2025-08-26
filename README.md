# MergeCopy

MergeCopy is a lightweight macOS menu bar utility for collecting and consolidating text snippets from your clipboard. It's designed to simplify gathering context for AI models.

## How It Works

The GIF below demonstrates the main workflow: activating recording mode, copying text from multiple sources, and then merging it all into the clipboard with a single click.

*[GIF placeholder]*

## Menu Options

### Idle Mode
*   **▶️ Start Recording**: Activates context-gathering mode.

### Recording Mode
*   **⏹️ Copy All**: Combines all captured text snippets, copies them to the clipboard, and ends the recording session.
*   **📄 Copy to File**: Saves the context to `context.txt` in your temporary directory, copies the file itself to the clipboard, and ends the session.
*   **🗑 Clear**: Discards the current session and all collected text, then stops recording.

## Download & Run

1.  **Download:** Get the `MergeCopy.zip` file from the [latest GitHub Release](https://github.com/mmvpm/MergeCopy/releases) and unzip it.

2.  **Authorize the App:** Before the first launch, macOS will show a security error ("damaged" or "from an unidentified developer"). This is a standard security measure. To fix this, open the **Terminal** app and run this one-time command:
    ```bash
    xattr -d com.apple.quarantine ~/Downloads/MergeCopy.app
    ```
    This command tells macOS to trust the application. You only need to do this once.

3.  **Launch:** You can now move `MergeCopy.app` to your **Applications** folder (or any other location) and open it.

*Note: If you prefer not to run the command above, you can build the app from source.*

## Building from Source

To build the `.app` from the source code, follow these steps.

1.  **Install Dependencies:**
    Open a terminal in the project folder and run:
    ```bash
    pip install -r requirements.txt py2app
    ```

2.  **Build the Application:**
    After installing the dependencies, run the build command:
    ```bash
    python setup.py py2app
    ```

3.  **Run:**
    A `dist` folder will be created containing `MergeCopy.app`. You can move this to your "Applications" folder and run it like any other app.
