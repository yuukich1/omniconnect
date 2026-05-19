from .base import SQLAlchemyRepository
from src.models import Chats

class ChatRepository(SQLAlchemyRepository):
    
    model = Chats