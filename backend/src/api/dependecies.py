from typing import Annotated
from fastapi import Depends

import src.services as srv
from src.core.config import oauth2_scheme
from src.core.exceptions.auth import TokenPayloadError
from src.schemas.users import CurrentUser
from src.core.config import settings

async def get_uow() -> srv.IUnitOfWork:
    return srv.UnitOfWork()

UowDep = Annotated[srv.IUnitOfWork, Depends(get_uow)]


_auth_service = srv.AuthService()
_security_service = srv.SecurityService()
_bots_service = srv.BotsService()
_tg_bot_service = srv.TelegramBotsService()
_messages_service = srv.MessageService()
_redis_broker_manager = srv.RedisMessageBroker(settings.REDIS_HOST, settings.REDIS_PORT)
_ws_manager = srv.WebsocketManager()
_conn_manager = srv.ConnectionManager()
_chat_service = srv.ChatService()


def get_auth_service() -> srv.AuthService:
    return _auth_service

def get_bots_service() -> srv.BotsService:
    return _bots_service

def get_tg_bot_service() -> srv.TelegramBotsService:
    return _tg_bot_service

def get_message_service() -> srv.MessageService:
    return _messages_service

def get_broker_manager() -> srv.RedisMessageBroker:
    return _redis_broker_manager

def get_ws_manager() -> srv.WebsocketManager:
    return _ws_manager

def get_conn_manager() -> srv.ConnectionManager:
    return _conn_manager

def get_chat_service() -> srv.ChatService:
    return _chat_service

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> CurrentUser:
    payload: dict = _security_service.decode_token(token)
    user_id_raw = payload.get("user_id")
    username = payload.get('username')
    role = payload.get('role')
    if not user_id_raw or not username or not role:
        raise TokenPayloadError
    return CurrentUser(
        id=int(user_id_raw),
        username=username,
        role=role
    )


AuthServiceDep = Annotated[srv.AuthService, Depends(get_auth_service)]
CurrentUserDep = Annotated[CurrentUser, Depends(get_current_user)]
BotsServiceDep = Annotated[srv.BotsService, Depends(get_bots_service)]
TelegramBotsServiceDep = Annotated[srv.TelegramBotsService, Depends(get_tg_bot_service)]
MessageServiceDep = Annotated[srv.MessageService, Depends(get_message_service)]
BrokerManagerDep = Annotated[srv.RedisMessageBroker, Depends(get_broker_manager)]
WSManagerDep = Annotated[srv.WebsocketManager, Depends(get_ws_manager)]
ConnManagerDep = Annotated[srv.ConnectionManager, Depends(get_conn_manager)]
ChatServiceDep = Annotated[srv.ChatService, Depends(get_chat_service)]