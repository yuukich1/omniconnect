from typing import List, Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, ForeignKey
from .base import BaseModel


class Chats(BaseModel):
    __tablename__ = 'chats'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    bot_id: Mapped[Optional[int]] = mapped_column(ForeignKey('bots.id'), nullable=True)
    chat_external_id: Mapped[int] = mapped_column(BigInteger, index=True, nullable=True) 
    
    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id', name='fk_chats_owner_id'))
    member_id: Mapped[Optional[int]] = mapped_column(ForeignKey('users.id', name='fk_chats_member_id'), nullable=True)
    
    username: Mapped[str] = mapped_column(nullable=False)

    messages: Mapped[List["Message"]] = relationship(
        "Message",
        backref="chat"
    )
    
    owner: Mapped["Users"] = relationship("Users", foreign_keys=[owner_id])
    member: Mapped[Optional["Users"]] = relationship("Users", foreign_keys=[member_id])