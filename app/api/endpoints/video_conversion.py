from fastapi import APIRouter, HTTPException

from app.services.summary_service import analyze_and_summarize_transcription
from app.services.video_conversion_service import download_video, convert_video_to_audio
from pydantic import BaseModel

from app.services.whisper_service import transcribe_audio_to_text_with_openai_api

router = APIRouter()


class VideoRequest(BaseModel):
    url: str


# @router.post("/convert-and-transcribe/")
# def convert_and_transcribe_video(request_body: VideoRequest):
#     try:
#         video_path = download_video(request_body.url)
#         audio_path = convert_video_to_audio(video_path)
#         transcribed_text = transcribe_audio_to_text_with_openai_api(audio_path)
#         return {"message": "Conversion and transcription successful", "audio_path": audio_path, "transcribed_text": transcribed_text}
#     except Exception as e:
#         print(f"Error in convert_and_transcribe_video: {e}")
#         raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze-transcription/")
def analyze_transcription(request_body: VideoRequest):
    try:
        video_path = download_video(request_body.url)
        audio_path = convert_video_to_audio(video_path)
        transcribed_text = transcribe_audio_to_text_with_openai_api(audio_path)
        analysis_result = analyze_and_summarize_transcription(transcribed_text)

        return analysis_result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
