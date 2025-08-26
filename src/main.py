import pyperclip
import rumps
import logging
import tempfile
import subprocess
import os

# --- Logger Setup ---
log_file = "merge_copy.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_file, mode='w'),
        logging.StreamHandler()
    ]
)

class ContextApp(rumps.App):
    """
    An application for collecting context with the ability to enable and disable recording mode.
    """
    def __init__(self, name, *args, **kwargs):
        # Pass quit_button='Quit' to super so that rumps creates and manages the exit button.
        # We can access this object through self.quit_button.
        super(ContextApp, self).__init__(name, quit_button='Quit', *args, **kwargs)
        
        logging.info("Application starting in idle mode...")
        
        self.is_recording = False
        self.captured_texts = []
        self.last_clipboard_content = ""
        
        self.clipboard_checker = rumps.Timer(self.check_clipboard, 0.75)
        self.clipboard_checker.start()

        # Set the initial menu. Rumps will add the Quit button on launch.
        self.menu = [
            rumps.MenuItem('▶️ Start Recording', callback=self.toggle_recording_state),
            None  # Add a separator for consistency
        ]

    def rebuild_menu(self):
        """
        Rebuilds the menu, preserving the original Quit button managed by rumps.
        This is the "native" way to work with a dynamic menu in rumps.
        """
        # 1. Save a reference to the native Quit button
        quit_button_instance = self.quit_button
        
        # 2. Clear the entire menu
        self.menu.clear()

        # 3. Build the new menu based on the state
        if not self.is_recording:
            self.menu.add(rumps.MenuItem('▶️ Start Recording', callback=self.toggle_recording_state))
        else:
            self.menu.add(rumps.MenuItem('⏹️ Copy All', callback=self.copy_and_stop))
            self.menu.add(rumps.MenuItem('📄 Copy to File', callback=self.copy_to_file_and_stop))
            self.menu.add(rumps.MenuItem('🗑 Clear', callback=self.clear_and_stop))
        
        # 4. Add back the separator and the original Quit button
        self.menu.add(None)
        self.menu.add(quit_button_instance)
            
    def toggle_recording_state(self, _):
        """Toggles the recording state."""
        self.is_recording = not self.is_recording
        
        if self.is_recording:
            self.captured_texts = []
            # Ignore the current content to avoid capturing it by mistake
            try:
                self.last_clipboard_content = pyperclip.paste() or ""
            except Exception:
                self.last_clipboard_content = ""

            logging.info("Recording started.")
            rumps.notification(
                title="Context recording started",
                subtitle="Copy text (Cmd+C) to add it.",
                message=""
            )
        else:
            logging.info("Recording stopped.")

        self.rebuild_menu()
        self.update_title()
        
    def copy_and_stop(self, _):
        """Copies the collected context and stops recording."""
        if not self.captured_texts:
            rumps.alert(title="Context is empty", message="You haven't copied anything in this session.")
        else:
            full_context = "\n\n---\n\n".join(self.captured_texts)
            pyperclip.copy(full_context)
            self.last_clipboard_content = full_context
            logging.info("Copied all collected text to clipboard.")
            rumps.notification(
                title="Context copied!",
                subtitle=f"All {len(self.captured_texts)} fragments are in your clipboard.",
                message="Recording stopped."
            )
        
        self.is_recording = False
        self.rebuild_menu()
        self.update_title()
        
    def copy_to_file_and_stop(self, _):
        """Saves the context to a file, copies the file to the clipboard, and stops recording."""
        if not self.captured_texts:
            rumps.alert(title="Context is empty", message="You haven't copied anything in this session.")
            self.is_recording = False
            self.rebuild_menu()
            self.update_title()
            return

        full_context = "\n\n---\n\n".join(self.captured_texts)
        
        try:
            temp_dir = tempfile.gettempdir()
            file_path = os.path.join(temp_dir, "context.txt")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(full_context)
            logging.info(f"Context saved to temporary file: {file_path}")

            applescript = f'set the clipboard to (POSIX file "{file_path}")'
            subprocess.run(['osascript', '-e', applescript], check=True, timeout=2)
            
            rumps.notification(
                title="File copied!",
                subtitle="The file context.txt is in your clipboard.",
                message="Recording stopped."
            )

        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, OSError) as e:
            logging.error(f"Failed to copy file to clipboard: {e}")
            rumps.alert(title="Error", message=f"Failed to copy the file to the clipboard.\n{e}")

        self.is_recording = False
        self.rebuild_menu()
        self.update_title()

    def clear_and_stop(self, _):
        """Clears the context and stops recording."""
        self.captured_texts = []
        self.last_clipboard_content = ""
        self.is_recording = False
        logging.info("Context cleared and recording stopped.")
        rumps.notification(title="Recording stopped", subtitle="The context has been cleared.", message="")
        self.rebuild_menu()
        self.update_title()

    def check_clipboard(self, _):
        """Checks the clipboard if the application is in recording mode."""
        if not self.is_recording:
            return

        try:
            current_clipboard = pyperclip.paste() or ""
            
            if current_clipboard and current_clipboard != self.last_clipboard_content:
                logging.info(f"New text detected: '{current_clipboard[:40]}...'")
                self.captured_texts.append(current_clipboard)
                self.last_clipboard_content = current_clipboard
                self.update_title()
                rumps.notification(
                    title="Context added",
                    subtitle=f"Total fragments: {len(self.captured_texts)}",
                    message=f"'{current_clipboard[:30]}...'"
                )
        except (pyperclip.PyperclipException, Exception) as e:
            logging.error(f"An error occurred in check_clipboard: {e}", exc_info=True)

    def update_title(self):
        """Updates the title to show the recording status and the number of fragments."""
        if self.is_recording:
            self.title = f"📋 {len(self.captured_texts)}"
        else:
            self.title = "📋"
    
    def run(self, *args, **kwargs):
        try:
            content = pyperclip.paste()
            self.last_clipboard_content = content if content is not None else ""
        except (pyperclip.PyperclipException, Exception):
             self.last_clipboard_content = ""
        logging.info(f"Initial clipboard content (will be ignored): '{self.last_clipboard_content[:30]}...'")

        self.update_title()
        logging.info("Starting rumps application run loop.")
        super(ContextApp, self).run(*args, **kwargs)


if __name__ == "__main__":
    app = ContextApp(name="MergeCopy")
    app.run()
