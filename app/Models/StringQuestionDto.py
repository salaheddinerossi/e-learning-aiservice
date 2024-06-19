from typing import List, Optional

from pydantic import BaseModel

class StringQuestionDto(BaseModel):
    id: int
    question: str
    answer: str
    correctAnswer: str

class MultipleChoiceQuestionsDto(BaseModel):
    transcribe: str
    stringQuestionDtos: List[StringQuestionDto]
