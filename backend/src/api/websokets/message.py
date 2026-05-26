from fastapi import APIRouter, Query, WebSocket, WebSocketDisconnect, status
from src.api.dependecies import WSManagerDep, get_current_user, BrokerManagerDep, TelegramBotsServiceDep, ConnManagerDep, UowDep, MessageServiceDep
from loguru import logger

websoket = APIRouter()

@websoket.websocket('/{chat_id}')
async def websoket_chat(
    websocket: WebSocket,
    chat_id: int,
    conn_manager: ConnManagerDep,
    tg_service: TelegramBotsServiceDep,
    borker: BrokerManagerDep,
    ws_manager: WSManagerDep,
    m_service: MessageServiceDep,
    uow: UowDep,
    token: str = Query(...)
):
    user = get_current_user(token)
    await conn_manager.connect(websocket, chat_id)
    try:
        while True:
            data = await websocket.receive_text()
            logger.info(data)
            await ws_manager.handle_message(data, chat_id, user, uow, borker, tg_service, conn_manager, m_service)
    except WebSocketDisconnect:
        conn_manager.disconnect(websocket, chat_id)
        