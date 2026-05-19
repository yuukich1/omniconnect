from .base import SQLAlchemyRepository, T
from src.models.message import Message


class MessageRepository(SQLAlchemyRepository):
    
    model = Message