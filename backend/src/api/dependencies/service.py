from typing import Annotated
from fastapi import Depends
from src.services.auth import AuthService
from src.services.uow import UnitOfWork
from src.services.security import SecurityService
from src.core.connection import async_session_maker
from src.services.users import UserService

_uow = UnitOfWork(async_session_maker)

_auth_service = AuthService()
_security_service = SecurityService()
_user_service = UserService()

UnitOfWorkDependency = Annotated[UnitOfWork, Depends(lambda: _uow)]
AuthServiceDependency = Annotated[AuthService, Depends(lambda: _auth_service)]
SecurityServiceDependency = Annotated[SecurityService, Depends(lambda: _security_service)]
UserServiceDependency = Annotated[UserService, Depends(lambda: _user_service)]
