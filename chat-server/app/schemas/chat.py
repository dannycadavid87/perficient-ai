from pydantic import BaseModel
from typing import List, Optional
from .user import UserOut
from datetime import datetime

class MessageOut(BaseModel):
    id: int
    sender_id: int
    content: str
    created_at: datetime
    model_config = {
        "from_attributes": True
    }

class ChatOut(BaseModel):
    id: int
    title: Optional[str]
    owner_id: int
    created_at: datetime
    messages: List[MessageOut] = []
    model_config = {
        "from_attributes": True
    }

class ChatCreate(BaseModel):
    title: Optional[str]
