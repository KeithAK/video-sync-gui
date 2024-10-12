import tkinter as tk
from tkinter import filedialog, Text
import subprocess

def select_destination_file():
    file_path = filedialog.askopenfilename(title="Select Destination Video")
    if file_path:
        destination_entry.delete(0, tk.END)
        destination_entry.insert(0, file_path)

def select_source_file():
    file_path = filedialog.askopenfilename(title="Select Source Video")
    if file_path:
        source_entry.delete(0, tk.END)
        source_entry.insert(0, file_path)

def select_output_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".mkv", title="Select Output File Location")
    if file_path:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, file_path)

def run_video_sync():
    destination_file = destination_entry.get()
    source_file = source_entry.get()
    output_file = output_entry.get()

    if destination_file and source_file and output_file:
        # Construct the command
        command = [
            "./bin/run", destination_file, source_file, 
            "-o", output_file,
            "-a", "ger",
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

# Run button
run_button = tk.Button(root, text="Run Video Sync", command=run_video_sync)
run_button.pack(pady=10)

# Start the main loop
root.mainloop()