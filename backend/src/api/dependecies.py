from typing import Annotated
from fastapi import Depends

import src.services as srv
from src.core.config import oauth2_scheme
from src.core.exceptions.auth import TokenPayloadError


async def get_uow() -> srv.IUnitOfWork:
    return srv.UnitOfWork()

UowDep = Annotated[srv.IUnitOfWork, Depends(get_uow)]


_auth_service = srv.AuthService()
_security_service = srv.SecurityService()
_bots_service = srv.BotsService()
_tg_bot_service = srv.TelegramBotsService()

def get_auth_service() -> srv.AuthService:
    return _auth_service

def get_bots_service() -> srv.BotsService:
    return _bots_service

def get_tg_bot_service() -> srv.TelegramBotsService:
    return _tg_bot_service

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> int:
    payload: dict = _security_service.decode_token(token)
    user_id_raw = payload.get("user_id")
    
    if user_id_raw is None:
        raise TokenPayloadError
    return int(user_id_raw)


AuthServiceDep = Annotated[srv.AuthService, Depends(get_auth_service)]
CurrentUserDep = Annotated[int, Depends(get_current_user)]
BotsServiceDep = Annotated[srv.BotsService, Depends(get_bots_service)]
TelegramBotsServiceDep = Annotated[srv.TelegramBotsService, Depends(get_tg_bot_service)]
