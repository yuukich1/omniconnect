from typing import Annotated
from fastapi import Depends
from src.services.auth import AuthService
from src.services.security import SecurityService
from src.services.users import UserService
from src.services.chats import ChatService
from src.services.message import MessageService


_auth_service = AuthService()
_security_service = SecurityService()
_user_service = UserService()
_chat_service = ChatService()
_message_service = MessageService()

AuthServiceDependency = Annotated[AuthService, Depends(lambda: _auth_service)]
SecurityServiceDependency = Annotated[SecurityService, Depends(lambda: _security_service)]
UserServiceDependency = Annotated[UserService, Depends(lambda: _user_service)]
ChatServiceDependency = Annotated[ChatService, Depends(lambda: _chat_service)]
MessageServiceDependecy = Annotated[MessageService, Depends(lambda: _message_service)]