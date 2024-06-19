from typing import List
from pydantic import BaseModel

class ExplanatoryQuestionsCorrectionResponse(BaseModel):
    advices: List[str] = []
    mark:float
