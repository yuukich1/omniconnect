from typing import Optional

from pydantic import BaseModel


class Chat(BaseModel):
    id: int
    username: str

class Chats(BaseModel):
    chats: Chat

