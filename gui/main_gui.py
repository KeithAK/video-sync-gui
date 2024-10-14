import tkinter as tk
from tkinter import filedialog, Text
import subprocess
import os

def select_destination_file():
    initial_path = "/Volumes/data/media"
    file_path = filedialog.askopenfilename(initialdir=initial_path, title="Select Destination Video")
    if file_path:
        destination_entry.delete(0, tk.END)
        destination_entry.insert(0, file_path)

def select_source_file():
    initial_path = "/Volumes/data/media/videos_edit/input"
    file_path = filedialog.askopenfilename(initialdir=initial_path, title="Select Source Video")
    if file_path:
        source_entry.delete(0, tk.END)
        source_entry.insert(0, file_path)

def select_output_file():
    initial_path = "/Users/keithknowles/Movies"

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

# Set up the GUI
root = tk.Tk()
root.title("Video Sync GUI")

# Destination video file selection
destination_label = tk.Label(root, text="Select Destination Video:")
destination_label.pack(pady=5)

destination_entry = tk.Entry(root, width=60)
destination_entry.pack(pady=5)

destination_button = tk.Button(root, text="Browse", command=select_destination_file)
destination_button.pack(pady=5)

# Source video file selection
source_label = tk.Label(root, text="Select Source Video:")
source_label.pack(pady=5)

source_entry = tk.Entry(root, width=60)
source_entry.pack(pady=5)

source_button = tk.Button(root, text="Browse", command=select_source_file)
source_button.pack(pady=5)

# Output video file selection
output_label = tk.Label(root, text="Select Output File Location:",)
output_label.pack(pady=5)

output_entry = tk.Entry(root, width=60,)
output_entry.pack(pady=5)

output_button = tk.Button(root, text="Browse", command=select_output_file)
output_button.pack(pady=5)

# Algorithm type dropdown menu
algorithm_label = tk.Label(root, text="Select Algorithm Type:")
algorithm_label.pack(pady=5)

algorithm_entry = tk.StringVar(root)
algorithm_entry.set("matching-scene")  # Default value

algorithm_menu = tk.OptionMenu(root, algorithm_entry, "matching-scene", "simple")
algorithm_menu.pack(pady=5)

# Run button
run_button = tk.Button(root, text="Run Video Sync", command=run_video_sync)
run_button.pack(pady=10)

# Result label
result_label = tk.Label(root, text="", fg="black", bg="white")
result_label.pack(pady=5)

# Start the main loop
root.mainloop()