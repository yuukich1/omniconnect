from datetime import datetime
from typing import List

from .base import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import func

    

class Attachments(BaseModel):
    
    __tablename__ = 'attachments'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    path: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    
    messages: Mapped[List["Message"]] = relationship(
        "Message",
        secondary="message_attachments",
        back_populates="attachments"
    )