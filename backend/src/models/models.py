from typing import List, Optional
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import JSONB
import uuid
from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property

from src.core.security import fernet 

class Base(DeclarativeBase):
    pass

class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        server_onupdate=func.now()
    )

class User(Base, TimestampMixin):
    __tablename__ = 'users'
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[str] = mapped_column(default='user')
    
    bots: Mapped[List["Bot"]] = relationship(back_populates="owner")
    chats: Mapped[List["Chat"]] = relationship(back_populates="owner")
    posts: Mapped[List["Post"]] = relationship(back_populates="author")

class Bot(Base, TimestampMixin):
    __tablename__ = 'bots'
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    platform: Mapped[str] = mapped_column(nullable=False)
    owner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('users.id'), index=True)
    _encrypted_token: Mapped[str] = mapped_column(nullable=False)
    
    owner: Mapped["User"] = relationship(back_populates="bots")
    chats: Mapped[List["Chat"]] = relationship(back_populates="bot")
    
    def __init__(self, **kwargs):
        token = kwargs.pop('token', None)
        super().__init__(**kwargs)
        if token is not None:
            self.token = token

    @hybrid_property
    def token(self) -> str: # type: ignore
        decrypted_bytes = fernet.decrypt(self._encrypted_token.encode())
        return decrypted_bytes.decode()
    
    @token.setter # type: ignore
    def token(self, raw_token: str):
        if not raw_token:
            raise ValueError('token cannot be empty')
        encrypted_token = fernet.encrypt(raw_token.encode())
        self._encrypted_token = encrypted_token.decode()

class Chat(Base, TimestampMixin):
    __tablename__ = 'chats'
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    bot_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey('bots.id'), index=True)
    owner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('users.id'), index=True)
    type: Mapped[str] = mapped_column(index=True)
    external_id: Mapped[Optional[str]] = mapped_column(index=True)
    
    bot: Mapped[Optional["Bot"]] = relationship(back_populates="chats")
    owner: Mapped["User"] = relationship(back_populates="chats")
    members: Mapped[List["ChatMembers"]] = relationship(back_populates="chat")
    messages: Mapped[List["Message"]] = relationship(back_populates="chat")

class ChatMembers(Base, TimestampMixin):
    __tablename__ = 'chat_members'
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    chat_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('chats.id', ondelete="CASCADE"), index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('users.id'), index=True)
    role: Mapped[str] = mapped_column(default='member')
    
    chat: Mapped["Chat"] = relationship(back_populates="members")

class Message(Base, TimestampMixin):
    __tablename__ = 'messages'
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    chat_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('chats.id', ondelete="CASCADE"), index=True)
    author_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey('users.id'), index=True)
    
    sender_metadata: Mapped[dict] = mapped_column(JSONB, default=dict)
    text: Mapped[Optional[str]] = mapped_column()
    media: Mapped[Optional[dict]] = mapped_column(JSONB)
    
    chat: Mapped["Chat"] = relationship(back_populates="messages")

class Post(Base, TimestampMixin):
    __tablename__ = 'posts'
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    author_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('users.id'), index=True)
    body: Mapped[Optional[str]] = mapped_column()
    
    author: Mapped["User"] = relationship(back_populates="posts")
    media: Mapped[list] = mapped_column(JSONB, default=list)
    stats: Mapped[dict] = mapped_column(JSONB, default={"views": 0, "likes": 0})
    

class RefreshToken(Base):
    __tablename__ = 'refresh_tokens'
    
    jti: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('users.id', ondelete="CASCADE"))
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    is_revoked: Mapped[bool] = mapped_column(default=False)
    user_agent: Mapped[Optional[str]] = mapped_column()
    ip_address: Mapped[Optional[str]] = mapped_column()
    
    user: Mapped["User"] = relationship("User", backref="refresh_tokens")