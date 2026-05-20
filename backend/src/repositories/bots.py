
from typing import Optional

from sqlalchemy import select

from .base import SQLAlchemyRepository, T
from src.models.bots import Bots
from src.models.chats import Chats


class BotsRepository(SQLAlchemyRepository):
    
    model = Bots
    
    async def get_by_platform(self, user_id: int, platform: str) -> Optional[Bots]:
        query = select(self.model).filter_by(user_id=user_id, platform=platform)
        bot = await self.session.execute(query)
        return bot.scalar_one_or_none()
    
    async def list_by_user_id(self, user_id: int) -> list[Bots]:
        query = select(self.model).filter_by(user_id=user_id)
        bots = await self.session.execute(query)
        return list(bots.scalars().all())
    
    async def get_chat_id(self, chat_id: int) -> Optional[Bots]:
        query = select(self.model).join(Chats, self.model.id == Chats.bot_id).filter(Chats.id == chat_id)
        bot = await self.session.execute(query)
        return bot.scalar_one_or_none()
    