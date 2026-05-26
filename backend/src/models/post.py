from datetime import datetime
from typing import List, Optional
from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import BaseModel

class Post(BaseModel):
    
    __tablename__ = 'post'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    
    attachments: Mapped[List["PostAttachment"]] = relationship(
        "PostAttachment",
        back_populates="post",
        cascade="all, delete-orphan"
    )
    
class PostAttachment(BaseModel):
    
    __tablename__ = 'post_attachment'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'), nullable=False)
    file_path: Mapped[str] = mapped_column(nullable=False)
    
    post: Mapped["Post"] = relationship("Post", back_populates="attachments")
    
