from typing import List, Optional

from pydantic import BaseModel

class BooleanQuestionDto(BaseModel):
    id: int
    question: str
    answer: bool
    correctAnswer: bool

class TrueFalseQuestionsDto(BaseModel):
    transcribe: str
    booleanQuestionDtos: List[BooleanQuestionDto]
