from typing import Optional
from sqlalchemy import select

from .base import SQLAlchemyRepository, T
from src.models.users import Users


class UserRepository(SQLAlchemyRepository):
    
    model = Users
    
    async def get_by_email(self, email: str) -> Optional[T]:
        query = select().filter_by(email=email)
        user = await self.session.execute(query)
        return user.scalar_one_or_none()
    
    async def get_by_username(self, username: str) -> Optional[T]:
        query = select().filter_by(username=username)
        user = await self.session.execute(query)
        return user.scalar_one_or_none()
