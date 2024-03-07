from fastapi import APIRouter, HTTPException
from app.services.video_conversion_service import download_video, convert_video_to_audio
from app.services.whisper_service import transcribe_audio_to_text_with_openai_api
from pydantic import BaseModel

router = APIRouter()

class VideoURL(BaseModel):
    url: str

@router.post("/convert-video/")
def convert_video(video_url: VideoURL):
    try:
        video_path = download_video(video_url.url)
        audio_path = convert_video_to_audio(video_path)
        return {"message": "Conversion successful", "audio_path": audio_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class VideoRequest(BaseModel):
    url: str

@router.post("/convert-and-transcribe/")
def convert_and_transcribe_video(request_body: VideoRequest):
    try:
        video_path = download_video(request_body.url)
        audio_path = convert_video_to_audio(video_path)
        transcribed_text = transcribe_audio_to_text_with_openai_api(audio_path)
        return {"message": "Conversion and transcription successful", "audio_path": audio_path, "transcribed_text": transcribed_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
