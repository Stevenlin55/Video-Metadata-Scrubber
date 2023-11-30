import subprocess
import json
import tkinter as tk
from tkinter import filedialog

def print_metadata_fields(metadata, current_field='', fields_list=[]):
    for key, value in metadata.items():
        if isinstance(value, dict):
            if current_field:
                current_field += '.'
            current_field += key
            print_metadata_fields(value, current_field, fields_list)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    print_metadata_fields(item, current_field, fields_list)
                else:
                    field_name = f"{current_field}.{item}" if current_field else item
                    field_value = metadata[key][item]
                    fields_list.append(f"{field_name}: {field_value}")
        else:
            field_name = f"{current_field}.{key}" if current_field else key
            field_value = value
            fields_list.append(f"{field_name}: {field_value}")


def get_metadata_value(metadata, field):
    fields = field.split('.')
    value = metadata
    for sub_field in fields:
        value = value.get(sub_field, {})
    return value


def remove_selected_metadata(input_video, fields_to_remove):
    ffmpeg_command = ["ffmpeg", "-i", input_video]

    # Add flags to clear all metadata
    ffmpeg_command.extend(["-map_metadata", "-1"])

    # Add flags to copy metadata for specific streams (e.g., video and audio)
    ffmpeg_command.extend(["-map_metadata:s:v", "0:s:v",
                          "-map_metadata:s:a", "0:s:a"])

    # Save the output video with the same extension as the input video
    output_extension = input_video.split('.')[-1]
    output_video = f"{input_video.rsplit('.', 1)[0]}_scrubbed.{output_extension}"
    ffmpeg_command.append(output_video)

    subprocess.run(ffmpeg_command)
    return output_video

def print_video_metadata(video_file):
    # Run ffprobe command and capture the output of the video file
    ffprobe_command = ["ffprobe", "-v", "quiet", "-print_format",
                       "json", "-show_format", "-show_streams", video_file]
    ffprobe_output = subprocess.check_output(
        ffprobe_command, stderr=subprocess.STDOUT, universal_newlines=True)

    # Parse and print the metadata of the video
    metadata = json.loads(ffprobe_output)

    print("Metadata of the output video:")
    print(json.dumps(metadata, indent=4))


def choose_video_file():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    file_path = filedialog.askopenfilename(title="Choose a Video File", filetypes=[("Video Files", "*.mp4 *.avi *.mkv *.mov *.flv *.wmv *.mpeg *.mpg")])

    return file_path

def main():
    input_video = choose_video_file()

    # Run ffprobe command and capture the output
    ffprobe_command = ["ffprobe", "-v", "quiet", "-print_format",
                       "json", "-show_format", "-show_streams", input_video]
    ffprobe_output = subprocess.check_output(
        ffprobe_command, stderr=subprocess.STDOUT, universal_newlines=True)

    # Parse the JSON output
    metadata = json.loads(ffprobe_output)

    # Get a list of available metadata fields
    available_fields = []
    print_metadata_fields(metadata, fields_list=available_fields)

    print("Available metadata fields:")
    for i, field in enumerate(available_fields):
        print(f"{i + 1}. {field}")

    # Ask the user to choose which fields to remove
    selected_indices = input(
        "Enter the numbers of the metadata fields to remove (comma-separated): ")
    selected_indices = [int(idx) for idx in selected_indices.split(",")]

    fields_to_remove = [available_fields[i - 1] for i in selected_indices]

    # Print the metadata fields and their values to be removed
    print("Metadata fields and their values to remove:")
    for field in fields_to_remove:
        field_name = field.split('.')[-1]
        field_value = get_metadata_value(metadata, field)
        print(f"{field_name}: {field_value}")

    # Remove selected metadata using FFmpeg
    output_video = remove_selected_metadata(
        input_video, fields_to_remove)

    print(
        f"Selected metadata fields removed successfully. Output file: {output_video}")

if __name__ == "__main__":
    main()
