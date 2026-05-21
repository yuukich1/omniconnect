from typing import Optional
from sqlalchemy import select

from src.models.token import RefreshToken

from .base import SQLAlchemyRepository, T
from src.models.users import Users

class UserRepository(SQLAlchemyRepository):
    
    model = Users
    
    async def get_by_email(self, email: str) -> Optional[Users]:
        query = select(self.model).filter_by(email=email)
        user = await self.session.execute(query)
        return user.scalar_one_or_none()
    
    async def get_by_username(self, username: str) -> Optional[Users]:
        query = select(self.model).filter_by(username=username)
        user = await self.session.execute(query)
        return user.scalar_one_or_none()
    
    async def get_user_by_token(self, token: str) -> Optional[Users]:
        query = select(self.model).join(RefreshToken, RefreshToken.user_id == Users.id).filter(RefreshToken.refresh_token == token, RefreshToken.blacklist == False)
        user = await self.session.execute(query)
        return user.scalar_one_or_none()
