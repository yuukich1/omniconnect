from typing import List, Optional

from sqlalchemy import or_, select

from src.models.bots import Bots

from .base import SQLAlchemyRepository
from src.models import Chats

class ChatRepository(SQLAlchemyRepository):
    
    model = Chats
    
    async def get_by_chat_id_and_bot_id(self, chat_id: int, bot_id: int) -> Optional[Chats]:  # noqa: F821
        query = select(self.model).filter_by(chat_external_id=chat_id, bot_id=bot_id)
        chat = await self.session.execute(query)
        return chat.scalar_one_or_none()
    
    async def list_by_user_id(self, user_id: int) -> List[Chats]:
        query = select(self.model).filter(
            or_(
                self.model.owner_id == user_id,
                self.model.member_id == user_id
            )
        )
        chats = await self.session.execute(query)
        return list(chats.scalars().all())