from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, validates
from .base import BaseModel
import hashlib

class Users(BaseModel):

    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    username: Mapped[str] = mapped_column(nullable=True, default=lambda context: context.current_parameters.get('email'), )
    hashed_password: Mapped[str] = mapped_column(nullable=False)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    @validates('hashed_password')
    def validate_password(self, key, password):
        if not password:
            raise ValueError('password cannot be empty')
        hashed = hashlib.sha256(password.encode()).hexdigest()
        return hashed
    
    def verify_password(self, password: str) -> bool:
        return self.hashed_password == hashlib.sha256(password.encode()).hexdigest()
    
