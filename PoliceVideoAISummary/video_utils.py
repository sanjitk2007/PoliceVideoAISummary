import os
import subprocess

def split_video_into_chunks(video_path, output_dir, chunk_length=300):
    os.makedirs(output_dir, exist_ok=True)
    
    output_pattern = os.path.join(output_dir, 'chunk_%03d.mp4')

    # build ffmeg command for splitting video into chunks
    cmd = [
        'ffmpeg',
        '-i', video_path,
        '-c', 'copy',
        '-map', '0',
        '-segment_time', str(chunk_length),
        '-f', 'segment',
        '-reset_timestamps', '1',
        output_pattern
    ]

    # run command as a subprocess
    subprocess.run(cmd, check=True)

    # return sorted list of chunks 
    return [os.path.join(output_dir, f) for f in sorted(os.listdir(output_dir)) if f.startswith('chunk_') and f.endswith('.mp4')] 