from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.quizz_generator_service import generate_quiz_from_transcription

router = APIRouter()


class TranscriptRequest(BaseModel):
    transcription: str
    additional_instructions: str


@router.post("/generate-quiz/")
def generate_mth_quiz(request: TranscriptRequest):
    try:
        quiz = generate_quiz_from_transcription(request.transcription, request.additional_instructions,
                                                "multiple-choice")
        return quiz
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate-true-false-quiz/")
def generate_true_false_quiz_router(request: TranscriptRequest):
    try:
        quiz = generate_quiz_from_transcription(request.transcription, request.additional_instructions, "true_false")
        return quiz
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate-explanatory-questions/")
def generate_explanatory_questions(request: TranscriptRequest):
    try:
        quiz = generate_quiz_from_transcription(request.transcription, request.additional_instructions, "explanatory")
        return quiz
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
