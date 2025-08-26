# MergeCopy

MergeCopy is a lightweight macOS menu bar utility for collecting and consolidating text snippets from your clipboard.

## How It Works

The GIF below demonstrates the main workflow: activating recording mode, copying text from multiple sources, and then merging it all into the clipboard with a single click.

*[GIF placeholder]*

## Download

You can download the latest version of `MergeCopy` app from the [GitHub Releases page](https://github.com/mmvpm/MergeCopy/releases). Just download the `.zip` archive from the latest release, unpack it, and move `MergeCopy` to your Applications folder.

## Menu Options

### Idle Mode
*   **▶️ Start Recording**: Activates context-gathering mode.

### Recording Mode
*   **⏹️ Copy All**: Combines all captured text snippets, copies them to the clipboard, and ends the recording session.
*   **📄 Copy to File**: Saves the context to `context.txt` in your temporary directory, copies the file itself to the clipboard, and ends the session.
*   **🗑 Clear**: Discards the current session and all collected text, then stops recording.

## Installation

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
