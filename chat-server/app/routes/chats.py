from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.auth.dependencies import get_current_user
from app.models.chat import Chat
from app.models.message import Message
from app.schemas.chat import ChatOut, ChatCreate, MessageOut
from app.schemas.message import MessageCreate
from typing import List

router = APIRouter(prefix="/chats", tags=["Chats"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[ChatOut], summary="List all chats of the authenticated user")
def list_chats(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    chats = db.query(Chat).filter(Chat.owner_id == int(current_user["sub"])).all()
    return chats

@router.get("/{id}", response_model=ChatOut, summary="Get the details of a chat")
def get_chat(id: int, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    chat = db.query(Chat).filter(Chat.id == id, Chat.owner_id == int(current_user["sub"])).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat

@router.get("/{id}/messages", response_model=List[MessageOut], summary="List the messages of a chat")
def list_messages(id: int, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    chat = db.query(Chat).filter(Chat.id == id, Chat.owner_id == int(current_user["sub"])).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat.messages

@router.post("/", response_model=ChatOut, summary="Creates a new chat")
def create_chat(chat: ChatCreate, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    db_chat = Chat(title=chat.title, owner_id=int(current_user["sub"]))
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return ChatOut.from_orm(db_chat)

@router.post("/{id}/messages", response_model=MessageOut, summary="Sends a new message to a chat")
def send_message(id: int, message: MessageCreate, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    chat = db.query(Chat).filter(Chat.id == id, Chat.owner_id == int(current_user["sub"])).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    db_message = Message(chat_id=id, sender_id=int(current_user["sub"]), content=message.content)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return MessageOut.from_orm(db_message)
