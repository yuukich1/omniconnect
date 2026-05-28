import uuid
from fastapi import APIRouter, Query, Request, WebSocket, WebSocketException, status
from src.api.dependencies.connect import ConnectManagerDepedency, UnitOfWorkDependency
from src.api.dependencies.service import MessageServiceDependecy
from src.api.dependencies.auth import get_current_user


websocket = APIRouter(prefix='/chats', tags=['chats'])

@websocket.websocket('/{chat_id}')
async def websocket_chat(websocket: WebSocket, chat_id: uuid.UUID, 
                         m_service: MessageServiceDependecy, conn_manager: ConnectManagerDepedency,
                         uow: UnitOfWorkDependency, access_token: str = Query(...)):
    user = get_current_user(access_token)
    if not user:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    await conn_manager.connect(websocket, chat_id)
    try:
        while True:
            data = await websocket.receive_json()
            text = data.get('text')
            media = data.get('media')
            await m_service.handle_message(chat_id, user, uow, conn_manager, text, media)
    except Exception as e:
        conn_manager.disconnect(websocket, chat_id)