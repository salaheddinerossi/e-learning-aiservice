from typing import List, Optional

from pydantic import BaseModel

class ExplanatoryQuestionDto(BaseModel):
    id: int
    question: str
    answer: str
    correctAnswer: str

class ExplanatoryQuestionsDto(BaseModel):
    transcribe: str
    explanatoryQuestionDtos: List[ExplanatoryQuestionDto]
