from typing import Optional
import uuid

from pydantic import BaseModel

class UserResponse(BaseModel):
    id: uuid.UUID
    username: str
    role: str
    

class UserUpdateRequest(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None
    

class UserChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str