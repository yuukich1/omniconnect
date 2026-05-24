from .base import SQLAlchemyRepository
from src.models.attachments import Attachments


class AttachmentsRepository(SQLAlchemyRepository):
    
    model = Attachments