from pydantic import BaseModel

class TokenDTO(BaseModel):
    access_token: str
    refresh_token: str
    jwi: str
    access_token_expires_in: int
    refresh_token_expires_in: int