import tkinter as tk
from tkinter import filedialog, ttk
import subprocess
import json
import os

# File where settings will be saved
SETTINGS_FILE = "gui_settings.json"

# Function to load settings from the JSON file
def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as file:
            return json.load(file)
    return {}

# Function to save settings to the JSON file
def save_settings():
    settings = {
        "default_dir_dest": entry_default_dir_dest.get(),
        "default_dir_src": entry_default_dir_src.get(),
        "default_dir_out": entry_default_dir_out.get(),
        "default_algorithm": algorithm_entry.get()
    }
    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file, indent=4)
    settings_status_label.config(text="Settings Saved!")

# Function to apply settings from the file (if they exist)
def apply_settings():
    settings = load_settings()
    if "default_dir_dest" in settings:
        entry_default_dir_dest.delete(0, tk.END)
        entry_default_dir_dest.insert(0, settings["default_dir_dest"])
    if "default_dir_src" in settings:
        entry_default_dir_src.delete(0, tk.END)
        entry_default_dir_src.insert(0, settings["default_dir_src"])
    if "default_dir_out" in settings:
        entry_default_dir_out.delete(0, tk.END)
        entry_default_dir_out.insert(0, settings["default_dir_out"])
    if "default_algorithm" in settings:
        algorithm_entry.set(settings["default_algorithm"])

def set_default_path_dest():
    dir_path = filedialog.askdirectory(initialdir=entry_default_dir_dest.get(), title="Select default directory for destination files")
    if dir_path:
        entry_default_dir_dest.delete(0, tk.END)
        entry_default_dir_dest.insert(0, dir_path)

def set_default_path_src():
    dir_path = filedialog.askdirectory(initialdir=entry_default_dir_src.get(), title="Select default directory for source files")
    if dir_path:
        entry_default_dir_src.delete(0, tk.END)
        entry_default_dir_src.insert(0, dir_path)

def set_default_path_out():
    dir_path = filedialog.askdirectory(initialdir=entry_default_dir_out.get(), title="Select default directory for output files")
    if dir_path:
        entry_default_dir_out.delete(0, tk.END)
        entry_default_dir_out.insert(0, dir_path)

def select_destination_file():
    file_path = filedialog.askopenfilename(initialdir=entry_default_dir_dest.get(), title="Select Destination Video")
    if file_path:
        destination_entry.delete(0, tk.END)
        destination_entry.insert(0, file_path)

def select_source_file():
    file_path = filedialog.askopenfilename(initialdir=entry_default_dir_src.get(), title="Select Source Video")
    if file_path:
        source_entry.delete(0, tk.END)
        source_entry.insert(0, file_path)

def select_output_file():
    initial_path = entry_default_dir_out.get()

    # Get the destination file name without the path and extension
    destination_file = destination_entry.get()
    if destination_file:
        base_filename = os.path.splitext(os.path.basename(destination_file))[0]
        initial_filename = f"{base_filename}"  # Suggest the same name as selected dest file
    else:
        initial_filename = "output"

    file_path = filedialog.asksaveasfilename(initialdir=initial_path, initialfile=initial_filename, defaultextension=".mkv", title="Select Output File Location")
    if file_path:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, file_path)

def run_video_sync():
    destination_file = destination_entry.get()
    source_file = source_entry.get()
    output_file = output_entry.get()
    algorithm_type = algorithm_entry.get()

    if destination_file and source_file and output_file:
        # Construct the command
        command = [
            "./bin/run", destination_file, source_file, 
            "-o", output_file,
            "-a", "ger",
            "-s", "ger",
            "-m", "60",
            "-g", algorithm_type,
            "-y",
            "-v"
        ]

        # Run the command using subprocess
        try:
            subprocess.run(command, check=True)

            result_label.config(text="Video sync completed successfully!")

        except subprocess.CalledProcessError as e:
            result_label.config(text=f"Error: {e}")
    else:
        result_label.config(text="Please select all files (destination, source, and output).")

# Set up the main GUI
root = tk.Tk()
root.title("Video Sync GUI")

# Create a Notebook (tabbed interface)
notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True)

# Tab 1: Main functionality
main_frame = ttk.Frame(notebook, width=400, height=400)
main_frame.pack(fill="both", expand=True)

# Destination video file selection
destination_label = tk.Label(main_frame, text="Select Destination Video:")
destination_label.pack(pady=5)

destination_entry = tk.Entry(main_frame, width=60)
destination_entry.pack(pady=5)

destination_button = tk.Button(main_frame, text="Browse", command=select_destination_file)
destination_button.pack(pady=5)

# Source video file selection
source_label = tk.Label(main_frame, text="Select Source Video:")
source_label.pack(pady=5)

source_entry = tk.Entry(main_frame, width=60)
source_entry.pack(pady=5)

source_button = tk.Button(main_frame, text="Browse", command=select_source_file)
source_button.pack(pady=5)

# Output video file selection
output_label = tk.Label(main_frame, text="Select Output File Location:",)
output_label.pack(pady=5)

output_entry = tk.Entry(main_frame, width=60)
output_entry.pack(pady=5)

output_button = tk.Button(main_frame, text="Browse", command=select_output_file)
output_button.pack(pady=5)

# Run button
run_button = tk.Button(main_frame, text="Run Video Sync", command=run_video_sync)
run_button.pack(pady=10)

# Result label
result_label = tk.Label(main_frame, text="", fg="black", bg="white")
result_label.pack(pady=5)

# Tab 2: Settings
settings_frame = ttk.Frame(notebook, width=400, height=400)
settings_frame.pack(fill="both", expand=True)

# default paths
lbl_default_dir_dest = tk.Label(settings_frame, text="Set default path: destination files")
lbl_default_dir_dest.pack(pady=5)
entry_default_dir_dest = tk.Entry(settings_frame, width=60)
entry_default_dir_dest.pack(pady=5)
btn_default_dir_dest = tk.Button(settings_frame, text="Set default path", command=set_default_path_dest)
btn_default_dir_dest.pack(pady=10)

lbl_default_dir_src = tk.Label(settings_frame, text="Set default path: source files")
lbl_default_dir_src.pack(pady=5)
entry_default_dir_src = tk.Entry(settings_frame, width=60)
entry_default_dir_src.pack(pady=5)
btn_default_dir_src = tk.Button(settings_frame, text="Set default path", command=set_default_path_src)
btn_default_dir_src.pack(pady=10)

lbl_default_dir_out = tk.Label(settings_frame, text="Set default path: dest files")
lbl_default_dir_out.pack(pady=5)
entry_default_dir_out = tk.Entry(settings_frame, width=60)
entry_default_dir_out.pack(pady=5)
btn_default_dir_out = tk.Button(settings_frame, text="Set default path", command=set_default_path_out)
btn_default_dir_out.pack(pady=10)

# Algorithm type dropdown menu
algorithm_label = tk.Label(settings_frame, text="Select Algorithm Type:")
algorithm_label.pack(pady=5)

algorithm_entry = tk.StringVar(settings_frame)
algorithm_entry.set("matching-scene")  # Default value

algorithm_menu = tk.OptionMenu(settings_frame, algorithm_entry, "matching-scene", "simple")
algorithm_menu.pack(pady=5)

# Button to save settings
save_settings_button = tk.Button(settings_frame, text="Save Settings", command=save_settings)
save_settings_button.pack(pady=10)

# Status label for settings save confirmation
settings_status_label = tk.Label(settings_frame, text="")
settings_status_label.pack(pady=5)

# Add tabs to the notebook
notebook.add(main_frame, text="Main")
notebook.add(settings_frame, text="Settings")

# Load and apply settings on start
apply_settings()

# Start the main loop
root.mainloop()