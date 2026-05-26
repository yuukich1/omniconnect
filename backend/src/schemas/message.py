from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List, Optional

class AttachmentSchema(BaseModel):
    id: int
    file_url: str 
    
    model_config = ConfigDict(from_attributes=True)

class MessageSchema(BaseModel):
    id: int
    chat_id: int
    text: Optional[str] = None
    is_from_bot: bool
    created_at: datetime
    # attachments: List[AttachmentSchema] = [] 
    
    model_config = ConfigDict(from_attributes=True)