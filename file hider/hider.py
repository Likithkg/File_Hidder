import os
import shutil
import random
import string
import tkinter as tk
from tkinter import filedialog, messagebox
import platform
import pyperclip  # Import the pyperclip library
import tempfile  # Import the tempfile module
import subprocess
def detect_os():
    system = platform.system()
    if system == 'Windows':
        windows()
    elif system == 'Darwin' or system == 'Linux':
        macOS()
    else:
        messagebox.showwarning("OS not supported")

def windows():
    root = tk.Tk()
    root.iconbitmap('icon.ico')  # Set the icon using the iconbitmap method
    root.geometry("1920x1080")  # Set the window size
    root.mainloop()

def macOS():
    root = tk.Tk()
    root.iconphoto(True, tk.PhotoImage(file="icon.jpg"))  # Set the icon using the iconphoto method
    root.geometry("1920x1080")  # Set the window size
    root.mainloop()

def random_string(length=8):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))

def hide_path(path):
    try:
        # Create a hidden directory in the system's temporary directory
        hidden_dir = os.path.join(tempfile.gettempdir(), random_string())
        os.makedirs(hidden_dir, exist_ok=True)
        
        # Move the file to the hidden directory
        shutil.move(path, hidden_dir)
        
        path_message = f"File hidden successfully at: {hidden_dir}"
        messagebox.showinfo("Success!", path_message)
        
        # Copy the path to the clipboard
        pyperclip.copy(hidden_dir)
        
        # Create a shortcut/icon for the application
        create_shortcut()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to hide file: {str(e)}")

def retrieve_path():
    try:
        # Prompt the user to select a file from the system's temporary directory
        path = filedialog.askopenfilename(title="Select hidden file", initialdir=tempfile.gettempdir())
        if path:
            base_name = os.path.basename(path)
            parent_dir = os.path.dirname(path)
            path_message = f"Hidden file '{base_name}' found at: '{parent_dir}'"
            messagebox.showinfo("Success", path_message)
            
            # Copy the path to the clipboard
            pyperclip.copy(parent_dir)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to retrieve the file: {str(e)}")

def browse_path():
    path = filedialog.askopenfilename(title="Select file to hide")
    if path:
        entry_path.delete(0, tk.END)
        entry_path.insert(0, path)

def create_shortcut():
    system = platform.system()
    if system == "Windows":
        try:
            from pyshortcuts import make_shortcut
            script_path = os.path.abspath(__file__)
            icon_path = os.path.abspath("icon.ico")  # Adjust the path to your icon file
            make_shortcut(script_path, name="File Hider", icon=icon_path)
        except ImportError:
            raise ImportError("pyshortcuts package is required for creating shortcuts on Windows.")
    elif system == "Darwin":
        try:
            script_path = os.path.abspath(__file__)
            icon_path = os.path.abspath("icon.jpg")  # Adjust the path to your icon file
            script = f'''
                tell application "Finder"
                    make alias file to (posix file "{script_path}" as alias) at POSIX file "{os.path.expanduser('~/Desktop')}"
                    set icon file of result to POSIX file "{icon_path}"
                end tell
            '''
            subprocess.run(['osascript', '-e', script])
        except Exception as e:
            raise RuntimeError(f"Failed to create shortcut on macOS: {e}")
    elif system == "Linux":
        try:
            desktop_dir = os.path.join(os.path.expanduser('~'), 'Desktop')
            shutil.copy(script_path, desktop_dir)
        except Exception as e:
            raise RuntimeError(f"Failed to create shortcut on Linux: {e}")
    else:
        raise NotImplementedError(f"Shortcut creation is not supported on {system}")

root = tk.Tk()
root.title("File Hider")
root.geometry("1920x1080")  # Set the window size

frame = tk.Frame(root)
frame.pack(pady=10, padx=10)

entry_path = tk.Entry(frame)
entry_path.pack(side=tk.LEFT, padx=5)

browse_button = tk.Button(frame, text="Browse", command=browse_path)
browse_button.pack(side=tk.LEFT, padx=5)

hide_button = tk.Button(root, text="Hide", command=lambda: hide_path(entry_path.get()))
hide_button.pack(pady=5)

retrieve_button = tk.Button(root, text="Retrieve", command=retrieve_path)
retrieve_button.pack(pady=5)

# Create a shortcut/icon for the application
create_shortcut()

root.mainloop()
