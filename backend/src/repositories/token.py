from typing import Optional
from sqlalchemy import select

from .base import SQLAlchemyRepository, T
from src.models.token import RefreshToken

class RefreshTokenRepository(SQLAlchemyRepository):
    
    model = RefreshToken