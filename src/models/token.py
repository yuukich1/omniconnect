from datetime import datetime
from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from .base import BaseModel


class RefreshToken(BaseModel):
    
    __tablename__ = 'refresh_token'
    
    refresh_token: Mapped[str] = mapped_column(primary_key=True, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    
    