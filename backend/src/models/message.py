from datetime import datetime
from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from .base import BaseModel


class Message(BaseModel):

    __tablename__ = 'message'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    bots_id: Mapped[int] = mapped_column(ForeignKey('bots.id'), nullable=False)
    text: Mapped[str]
    attachments_url: Mapped[str] 
    created_at: Mapped[str] = mapped_column(server_default=func.now())


