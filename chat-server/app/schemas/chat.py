from pydantic import BaseModel
from typing import List, Optional
from .user import UserOut

class MessageOut(BaseModel):
    id: int
    sender_id: int
    content: str
    created_at: str
    class Config:
        orm_mode = True

class ChatOut(BaseModel):
    id: int
    title: Optional[str]
    owner_id: int
    created_at: str
    messages: List[MessageOut] = []
    class Config:
        orm_mode = True

class ChatCreate(BaseModel):
    title: Optional[str]
