from typing import List

from fastapi import HTTPException, APIRouter
from openai import BaseModel

from app.Models.Message import Message
from app.services.chat_service import reply_to_chat_with_context

router = APIRouter()

class ChatRequestDto(BaseModel):
    messages: List[Message]

@router.post("/chat/")
def chat_endpoint(request: ChatRequestDto):
    try:
        formatted_messages = [{"role": msg.role, "content": msg.content} for msg in request.messages]

        reply = reply_to_chat_with_context(formatted_messages)

        return {"reply": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
