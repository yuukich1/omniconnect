import uuid

from pydantic import BaseModel

class CreateBaseResponse(BaseModel):
    id: uuid.UUID
    
class StatusReponse(BaseModel):
    status: str = 'ok'