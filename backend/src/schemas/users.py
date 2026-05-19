import re
from typing import Annotated

from pydantic import BaseModel, EmailStr, Field, AfterValidator

def check_password_strength(v: str) -> str:
    if not re.search(r"\d", v):
        raise ValueError("Пароль должен содержать цифру")
    if not re.search(r"[A-ZА-Я]", v):
        raise ValueError("Пароль должен содержать заглавную букву")
    return v

class UserRegister(BaseModel):
    email: EmailStr
    username: str = Field(max_length=20)
    password: Annotated[str, Field(min_length=8, max_length=64), AfterValidator(check_password_strength)]
    
    