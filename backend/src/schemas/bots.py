from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum

class PlatformEnum(str, Enum):
    telegram = "telegram"
    discord = 'discrod'

class BotCreateRequest(BaseModel):
    platform: PlatformEnum
    token: str
    
class UpdateTokenRequest(BaseModel):
    token: str 
    
class BotResponse(BaseModel):
    id: int
    user_id: int
    platform: str
    
    created_at: datetime

    class ConfigDict:
        from_attributes = True
        

class TelegramMessageDTO(BaseModel):
    chat_id: int = Field(...)
    username: str = Field(default="unknown")
    text: Optional[str] = Field(default=None)
    file_id: Optional[str] = Field(default=None)
    file_name: Optional[str] = Field(default=None)
    media_type: str = Field(default="text")
    
    