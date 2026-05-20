from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, func
from sqlalchemy.ext.hybrid import hybrid_property
from .base import BaseModel
from src.core.config import fernet


class Bots(BaseModel):

    __tablename__ = 'bots'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    platform: Mapped[str] = mapped_column(nullable=False, index=True)
    _encrypted_token: Mapped[str] = mapped_column('token', nullable=False)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    
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
