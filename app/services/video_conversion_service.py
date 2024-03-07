from yt_dlp import YoutubeDL
from moviepy.editor import VideoFileClip
import os

def download_video(url: str, download_path: str = './videos') -> str:
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    ydl_opts = {'outtmpl': f'{download_path}/%(title)s.%(ext)s'}
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        info_dict = ydl.extract_info(url, download=False)
        video_title = info_dict.get('title', 'downloaded_video').replace("/", "_")  # Avoid path issues
        video_ext = info_dict.get('ext', 'mp4')
    return f"{download_path}/{video_title}.{video_ext}"

def convert_video_to_audio(video_path: str, audio_path: str = './audios') -> str:
    if not os.path.exists(audio_path):
        os.makedirs(audio_path)
    output_path = f"{audio_path}/{video_path.split('/')[-1].split('.')[0]}.mp3"
    video_clip = VideoFileClip(video_path)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(output_path, codec='mp3')
    audio_clip.close()
    video_clip.close()
    return output_path
