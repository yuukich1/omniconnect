from datetime import datetime
from typing import List, Optional
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
        

# class TelegramMessageDTO(BaseModel):
#     chat_id: int = Field(...)
#     username: str = Field(default="unknown")
#     text: Optional[str] = Field(default=None)
#     file_id: Optional[str] = Field(default=None)
#     file_name: Optional[str] = Field(default=None)
#     media_type: str = Field(default="text")
    
    
class TelegramMessageDTO(BaseModel):
    chat_id: int
    username: str
    text: Optional[str] = None
    file_id: Optional[str] = None 
    file_ids: List[str] = Field(default_factory=list) 
    media_group_id: Optional[str] = None
    file_name: str = "unknown_file"
    media_type: str = "text"
    