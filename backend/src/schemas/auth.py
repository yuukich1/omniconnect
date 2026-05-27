import uuid

from pydantic import BaseModel


class AuthRequest(BaseModel):
    username: str 
    password: str
    

class CurrentUser(BaseModel):
    id: uuid.UUID
    username: str
    role: str

class TokenReponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'
    expires_in: int