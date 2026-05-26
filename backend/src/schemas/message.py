from datetime import datetime

from pydantic import BaseModel, ConfigDict, model_validator
from typing import List, Optional, Any

class MessageSchema(BaseModel):
    id: int
    text: Optional[str] = None
    is_from_bot: bool
    created_at: datetime
    username: str
    files: List[str] = []

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode='after')
    def map_attachments_to_files(self) -> 'MessageSchema':
        return self

    @model_validator(mode='before')
    @classmethod
    def transform_attachments(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            if hasattr(data, 'attachments') and data.attachments:

                files = [f"/static/{att.path.replace(chr(92), '/')}" for att in data.attachments]
                

                data_dict = {
                    "id": data.id,
                    "text": data.text,
                    "is_from_bot": data.is_from_bot,
                    "created_at": data.created_at,
                    "username": data.username,
                    "files": files
                }
                return data_dict
            else:
                if hasattr(data, '__dict__'):
                    d = data.__dict__.copy()
                    d['files'] = []
                    return d
        return data