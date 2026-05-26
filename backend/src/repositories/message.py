from typing import Any, List, Optional

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from .base import SQLAlchemyRepository
from src.models.message import Message, MessageAttachments


class MessageRepository(SQLAlchemyRepository):
    
    model = Message
    
    async def get_messages_by_chat_id(self, chat_id: int, show: int) -> List[Message]:
        query = select(self.model).filter_by(chat_id=chat_id).order_by(self.model.created_at).limit(show)
        result = await self.session.execute(query)
        return list(result.scalars().all())
    
    async def get_by_media_group(self, media_group_id) -> Optional[Message]:
        query = select(Message).filter_by(media_group_id=media_group_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    
    async def get_messages_with_attachments_by_chat_id(self, chat_id: int, limit: int) -> List[Message]:
        query = (
            select(self.model)
            .options(joinedload(self.model.attachments)) 
            .filter_by(chat_id=chat_id)
            .order_by(self.model.created_at.desc()) 
            .limit(limit)
        )
        result = await self.session.execute(query)
        return list(result.unique().scalars().all())
    
    async def get_full_message_by_id(self, message_id: int) -> Optional[Message]:
        query = (
            select(self.model)
            .options(joinedload(self.model.attachments)) 
            .filter(self.model.id == message_id)
        )
        result = await self.session.execute(query)
        message = result.unique().scalar_one_or_none()
                
        return message
    
    
class MessageAttachmetsRepository(SQLAlchemyRepository):
    
    model = MessageAttachments
    
    async def exists(self, message_id: int, attachment_id_or_path: Any) -> bool:  

        query = select(self.model).where(
            self.model.message_id == message_id,
            self.model.attachments_id == attachment_id_or_path
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none() is not None