from .base import SqlAclehmyRepository
from src.models import Message


class MessageRepository(SqlAclehmyRepository):
    
    model = Message