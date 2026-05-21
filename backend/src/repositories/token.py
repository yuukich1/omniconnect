from typing import Optional
from sqlalchemy import update

from .base import SQLAlchemyRepository, T
from src.models.token import RefreshToken

class RefreshTokenRepository(SQLAlchemyRepository):
    
    model = RefreshToken
    
    
    async def add_to_blacklist(self, token: str) -> None:
        query = update(RefreshToken).where(RefreshToken.refresh_token == token).values(blacklist=True)
        await self.session.execute(query)