from typing import List
from pydantic import BaseModel

class CorrectionResponse(BaseModel):
    advices: List[str] = []
