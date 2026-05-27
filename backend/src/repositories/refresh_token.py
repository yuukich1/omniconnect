from typing import Optional

from sqlalchemy import select

from .base import SqlAclehmyRepository
from src.models.models import RefreshToken

class RefreshTokenRepository(SqlAclehmyRepository):
    
    model = RefreshToken
    
    async def get_by_jti(self, jti: str) -> Optional[RefreshToken]:
        result = await self.session.execute(
            select(self.model).where(self.model.jti == jti)
        )
        return result.scalar_one_or_none()
        