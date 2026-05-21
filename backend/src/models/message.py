from datetime import datetime
from typing import Optional
from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from .base import BaseModel


class Message(BaseModel):

    __tablename__ = 'message'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey('chats.id'), nullable=False)
    text: Mapped[Optional[str]] = mapped_column(default=None)
    attachments_url: Mapped[Optional[str]] = mapped_column(default=None) 
    username: Mapped[str] = mapped_column(server_default='unknown')
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    

