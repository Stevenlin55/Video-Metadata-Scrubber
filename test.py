import subprocess

# Replace 'input.mp4' with your actual input file and 'output.mp4' with the desired output file
input_filename = 'video.mov'
output_filename = 'output.mov'

# Define the fields you want to remove
fields_to_remove = [
    'creation_time',
    'encoder',
    'handler_name',
    'timecode',
    'location',
    'genre',
    'creator',
    'rating'
]

# Run FFmpeg to remove the specified fields from the metadata
subprocess.run([
    'ffmpeg',
    '-i', input_filename,
    '-c:v', 'copy',
    '-c:a', 'copy',
    '-map_metadata', '-1',
    '-map_metadata', '0',
    '-metadata', ','.join([f'{field}=' for field in fields_to_remove]),
    output_filename
])
