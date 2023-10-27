import subprocess
import json
import os

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
                    fields_list.append(f"{current_field}.{item}" if current_field else item)
        else:
            fields_list.append(f"{current_field}.{key}" if current_field else key)

def get_metadata_value(metadata, field):
    fields = field.split('.')
    value = metadata
    for sub_field in fields:
        value = value.get(sub_field, {})
    return value

def remove_selected_metadata(input_video, fields_to_remove):
    ffmpeg_command = ["ffmpeg", "-i", input_video]
    # remove the metadata fields from the input video
    for field in fields_to_remove:
        ffmpeg_command.extend(["-metadata", f"{field}="])
   
    # save the output video with the same extension as the input video
    output_extension = input_video.split('.')[-1]
    output_video = f"{input_video.rsplit('.', 1)[0]}_updated.{output_extension}"
    ffmpeg_command.append(output_video)
    subprocess.run(ffmpeg_command)
    return output_video

def print_video_metadata(video_file):
    # Run ffprobe command and capture the output of the video file
    ffprobe_command = ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", "-show_streams", video_file]
    ffprobe_output = subprocess.check_output(ffprobe_command, stderr=subprocess.STDOUT, universal_newlines=True)

    # Parse and print the metadata of the video
    metadata = json.loads(ffprobe_output)

    print("Metadata of the output video:")
    print(json.dumps(metadata, indent=4))

def main():
    # List all input video files in the script's directory
    script_directory = os.path.dirname(os.path.abspath(__file__))
    input_files = [f for f in os.listdir(script_directory) if f.endswith(('.mp4', '.mov'))]

    print("Available input video files:")
    for i, file in enumerate(input_files):
        print(f"{i + 1}. {file}")

    # Ask the user to choose an input file
    selected_index = input("Enter the number of the input video file you want to process: ")
    selected_index = int(selected_index)
    if selected_index < 1 or selected_index > len(input_files):
        print("Invalid selection. Please choose a valid number.")
        return

    selected_input_file = input_files[selected_index - 1]
    
    # Run ffprobe command and capture the output
    ffprobe_command = ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", "-show_streams", selected_input_file]
    ffprobe_output = subprocess.check_output(ffprobe_command, stderr=subprocess.STDOUT, universal_newlines=True)

    # Parse the JSON output
    metadata = json.loads(ffprobe_output)

    # Get a list of available metadata fields
    available_fields = []
    print_metadata_fields(metadata, fields_list=available_fields)

    print("Available metadata fields:")
    for i, field in enumerate(available_fields):
        field_name = field.split('.')[-1]
        field_value = get_metadata_value(metadata, field)
        print(f"{i + 1}. {field_name}: {field_value}")

    # Ask the user to choose which fields to remove
    selected_indices = input("Enter the numbers of the metadata fields to remove (comma-separated): ")
    selected_indices = [int(idx) for idx in selected_indices.split(",")]

    fields_to_remove = [available_fields[i - 1] for i in selected_indices]

    # Print the metadata fields and their values to be removed
    print("Metadata fields and their values to remove:")
    for field in fields_to_remove:
        field_name = field.split('.')[-1]
        field_value = get_metadata_value(metadata, field)
        print(f"{field_name}: {field_value}")

    # Remove selected metadata using FFmpeg
    output_video = remove_selected_metadata(selected_input_file, fields_to_remove)

    print(f"Selected metadata fields removed successfully. Output file: {output_video}")

    # Print metadata of the output video
    # print_video_metadata(output_video)

if __name__ == "__main__":
    main()
