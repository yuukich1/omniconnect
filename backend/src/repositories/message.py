from typing import List

from sqlalchemy import select

from .base import SQLAlchemyRepository
from src.models.message import Message


class MessageRepository(SQLAlchemyRepository):
    
    model = Message
    
    async def get_messages_by_chat_id(self, chat_id: int, show: int) -> List[Message]:
        query = select(self.model).filter_by(chat_id=chat_id).order_by(self.model.created_at).limit(show)
        result = await self.session.execute(query)
        return list(result.scalars().all())