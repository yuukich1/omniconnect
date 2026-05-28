from typing import Any, Dict, Optional
import uuid

from pydantic import BaseModel


class MessageResponse(BaseModel):
    id: uuid.UUID
    author_id: Optional[uuid.UUID] = None
    sender_metadata: Dict[str, Any]
    text: Optional[str] = None
    media: Optional[Dict] = None
    
#  message_model = await uow.message.create(Message(
#                 chat_id=chat_id,
#                 author_id=user.id,
#                 sender_metadata={
#                     'display_name': user.username,
#                     'is_bot': False,
#                     'api_version': settings.api_version,
#                     'user_agent': user_agent
#                 },
#                 text=text,
#                 # media
#             ))