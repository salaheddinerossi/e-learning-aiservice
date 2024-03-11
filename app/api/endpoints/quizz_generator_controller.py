from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.quizz_generator_service import generate_quiz_from_transcription

router = APIRouter()
class TranscriptRequest(BaseModel):
    transcription: str

@router.post("/generate-quiz/")
def generate_mth_quiz(request: TranscriptRequest):
    try:
        quiz = generate_quiz_from_transcription(request.transcription, "multiple-choice")
        return {"quiz": quiz}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-true-false-quiz/")
def generate_true_false_quiz_router(request: TranscriptRequest):
    try:
        quiz = generate_quiz_from_transcription(request.transcription, "true_false")
        return {"quiz": quiz}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-explanatory-questions/")
def generate_explanatory_questions(request: TranscriptRequest):
    try:
        quiz = generate_quiz_from_transcription(request.transcription, "explanatory")
        return {"quiz": quiz}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
