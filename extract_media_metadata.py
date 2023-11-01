import subprocess
import json
import tkinter as tk
from tkinter import filedialog

def get_all_video_metadata(input_video):
    # Run ffprobe to get all metadata as JSON 
    ffprobe_command = ["ffprobe", "-v", "quiet", "-print_format",
        "json", "-show_format", "-show_streams", input_video]
    
    ffprobe_output = subprocess.check_output(
        ffprobe_command, stderr=subprocess.STDOUT, universal_newlines=True)
    
    # Parse and return the metadata of the video
    metadata = json.loads(ffprobe_output)
    return metadata

def choose_video_file():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    file_path = filedialog.askopenfilename(title="Choose a Video File", filetypes=[("Video Files", "*.mp4 *.avi *.mkv *.mov *.flv *.wmv *.mpeg *.mpg")])

    return file_path

if __name__ == "__main__":
    input_video = choose_video_file()
    
    if input_video:
        metadata = get_all_video_metadata(input_video)
        if metadata:
            print("All Video Metadata:")
            print(json.dumps(metadata, indent=4))
        else:
            print("Failed to retrieve metadata.")
    else:
        print("No video file selected.")
