from typing import Optional

from sqlalchemy import select

from .base import SqlAclehmyRepository
from src.models.models import User

class UserRepository(SqlAclehmyRepository):
    
    model = User
    
    async def get_by_username(self, username: str) -> Optional[User]:
        result = await self.session.execute(
            select(self.model).where(self.model.username == username)
        )
        return result.scalar_one_or_none()