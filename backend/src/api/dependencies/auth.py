from typing import Annotated
import uuid
from fastapi import Depends
import jwt
from src.schemas.auth import CurrentUser
from src.services.security import SecurityService
from src.core.security import oauth2_scheme
from src.api.exceptions import exceptions as exc

_security_service = SecurityService()


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> CurrentUser:
    payload: dict = _security_service.verify_token(token, token_type='access')
    user_id_raw = payload.get("sub")
    username = payload.get('username')
    role = payload.get('role')
    if not user_id_raw or not username or not role:
        raise jwt.InvalidTokenError
    return CurrentUser(
        id=uuid.UUID(user_id_raw),
        username=username,
        role=role
    )

def get_current_admin_user(user: Annotated[CurrentUser, Depends(get_current_user)]) -> CurrentUser:
    if user.role != 'admin':
        raise exc.ForbidenError
    return user
    

CurrentUserDependency = Annotated[CurrentUser, Depends(get_current_user)]
CurrentAdminDependecy = Annotated[CurrentUser, Depends(get_current_admin_user)]
