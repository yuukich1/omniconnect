from datetime import datetime
from typing import List, Optional
from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel


class Message(BaseModel):
    
    __tablename__ = 'message'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey('chats.id'), nullable=False)
    text: Mapped[Optional[str]] = mapped_column(default=None)
    media_group_id: Mapped[Optional[str]] = mapped_column(index=True, nullable=True)
    is_from_bot: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    
    attachments: Mapped[List["Attachments"]] = relationship(
        "Attachments",
        secondary="message_attachments",
        back_populates="messages"
    )

class MessageAttachments(BaseModel):
    
    __tablename__ = 'message_attachments'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    message_id: Mapped[int] = mapped_column(ForeignKey('message.id'), nullable=False)
    attachments_id: Mapped[int] = mapped_column(ForeignKey('attachments.id'), nullable=False)