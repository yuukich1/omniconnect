
from typing import Optional

from sqlalchemy import select

from .base import SQLAlchemyRepository, T
from src.models.bots import Bots


class BotsRepository(SQLAlchemyRepository):
    
    model = Bots
    
    async def get_by_platform(self, user_id: int, platform: str) -> Optional[T]:
        query = select().filter_by(user_id=user_id, platform=platform)
        bot = await self.session.execute(query)
        return bot.scalar_one_or_none()
    