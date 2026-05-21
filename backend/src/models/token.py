from datetime import datetime
from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from .base import BaseModel


class RefreshToken(BaseModel):
    
    __tablename__ = 'refresh_token'
    
    refresh_token: Mapped[str] = mapped_column(primary_key=True, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    blacklist: Mapped[bool] = mapped_column(default=False, nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    
    