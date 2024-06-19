from fastapi import APIRouter, HTTPException

from app.Models.ExplanatoryQuestionsDto import ExplanatoryQuestionsDto
from app.Models.ExplanatoryQuestionsCorrectionResponse import ExplanatoryQuestionsCorrectionResponse
from app.Models.TrueFalseQuestionsDto import TrueFalseQuestionsDto
from app.Models.CorrectionResponse import CorrectionResponse
from app.Models.StringQuestionDto import MultipleChoiceQuestionsDto

from app.services.quizz_correction_service import correct_multiple_choice_quiz, correct_true_false_quiz, \
    correct_explanatory_quiz

router = APIRouter()

@router.post("/correction/multiple-choice", response_model=CorrectionResponse)
def multiple_choice_correction_endpoint(request: MultipleChoiceQuestionsDto):
    try:
        advice_response = correct_multiple_choice_quiz(request.transcribe, request.stringQuestionDtos)
        print(advice_response)
        return advice_response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/correction/true-false", response_model=CorrectionResponse)
def true_false_correction_endpoint(request: TrueFalseQuestionsDto):
    try:
        advice_response = correct_true_false_quiz(request.transcribe, request.booleanQuestionDtos)
        print(advice_response)
        return advice_response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/correction/explanatory", response_model=ExplanatoryQuestionsCorrectionResponse)
def explanatory_correction_endpoint(request: ExplanatoryQuestionsDto):
    try:
        correction_response = correct_explanatory_quiz(request.transcribe, request.explanatoryQuestionDtos)
        return correction_response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

