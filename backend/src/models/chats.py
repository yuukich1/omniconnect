from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, ForeignKey
from .base import BaseModel

class Chats(BaseModel):
    
    __tablename__ = 'chats'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    bot_id: Mapped[int] = mapped_column(ForeignKey('bots.id'), nullable=False)
    username: Mapped[str] = mapped_column(nullable=False)
    chat_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True)
    
    