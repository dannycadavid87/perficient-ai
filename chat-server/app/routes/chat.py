from fastapi import APIRouter
from app.models.chat import ChatRequest, ChatResponse
from app.services.chatbot import get_chat_response

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    response = get_chat_response(request.message)
    return ChatResponse(response=response)
