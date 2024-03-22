
from fastapi import HTTPException, APIRouter
from pydantic import BaseModel  # Corrected import

from app.services.summary_types_service import generate_summaries

router = APIRouter()


class SummaryRequest(BaseModel):  # Define the request body model
    transcribtion: str
    summary_type: str
    additional_instructions: str


@router.post("/generate-summary/")
def chat_endpoint(request: SummaryRequest):

    try:
        reply = generate_summaries(request.transcribtion,request.summary_type ,request.additional_instructions)

        return reply
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
