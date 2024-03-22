from yt_dlp import YoutubeDL
from moviepy.editor import VideoFileClip
import os
import uuid

def download_video(url: str, download_path: str = './videos') -> str:
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    unique_filename_prefix = str(uuid.uuid4())
    # Set a wildcard pattern for the output template to catch the extension.
    ydl_opts = {
        'outtmpl': os.path.join(download_path, unique_filename_prefix + '.%(ext)s'),
    }

    with YoutubeDL(ydl_opts) as ydl:
        # Download the video. The filename will be the unique identifier followed by the actual video extension.
        ydl.download([url])

    # Scan the directory for the file that starts with the unique prefix.
    for filename in os.listdir(download_path):
        if filename.startswith(unique_filename_prefix):
            # Found the downloaded file matching our unique prefix.
            return os.path.join(download_path, filename)

    # If no file is found, raise an error.
    raise FileNotFoundError(f"No downloaded file found with prefix {unique_filename_prefix} in {download_path}")

def convert_video_to_audio(video_path: str, audio_path: str = './audios') -> str:
    if not os.path.exists(audio_path):
        os.makedirs(audio_path)

    # Prepare the output audio path with the same base name as the video file but with an .mp3 extension.
    base_filename = os.path.splitext(os.path.basename(video_path))[0]
    output_path = os.path.join(audio_path, base_filename + '.mp3')

    # Convert the video to audio using MoviePy.
    video_clip = VideoFileClip(video_path)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(output_path, codec='mp3')
    audio_clip.close()
    video_clip.close()

    return output_path
