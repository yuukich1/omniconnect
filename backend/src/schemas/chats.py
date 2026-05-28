from datetime import datetime
import uuid

from pydantic import BaseModel
from typing import List, Optional
from src.enum import chats as ch_enum

class ChatCreateRequest(BaseModel):
    type: ch_enum.ChatType
    member_id: Optional[uuid.UUID] = None

class UserShortDTO(BaseModel):
    id: uuid.UUID
    username: str

class ChatDTO(BaseModel):
    id: uuid.UUID
    type: str
    members: List[UserShortDTO]
    created_at: datetime

    class Config:
        from_attributes = True
    
