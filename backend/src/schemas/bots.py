from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class BotCreateRequest(BaseModel):
    platform: str
    token: str
    
class BotResponse(BaseModel):
    id: int
    user_id: int
    platform: str
    
    token: str
    
    created_at: datetime

    class ConfigDict:
        from_attributes = True
        

class TelegramMessageDTO(BaseModel):
    chat_id: int = Field(..., description="ID чата/пользователя в Telegram")
    username: str = Field(default="unknown", description="Никнейм пользователя")
    text: Optional[str] = Field(default=None, description="Текст сообщения или подпись к медиа")
    file_id: Optional[str] = Field(default=None, description="ID файла на серверах Telegram")
    file_name: Optional[str] = Field(default=None, description="Имя сохраненного файла")
    media_type: str = Field(default="text", description="Тип контента: text, photo или document")
    
    