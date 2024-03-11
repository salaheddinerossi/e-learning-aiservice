from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.quizz_correction_service import correct_quiz

router = APIRouter()

class Correction(BaseModel):
    transcription: str
    quizz: str
    quiz_type: str  # Ensure this is included

@router.post("/correction/")
def chat_endpoint(request_body: Correction):
    try:
        reply = correct_quiz(request_body.transcription, request_body.quizz, request_body.quiz_type)
        return {"reply": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
