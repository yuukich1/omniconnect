from fastapi import APIRouter, Path, Request
from src.api.dependecies import TelegramBotsServiceDep, UowDep, WSManagerDep, get_current_user, BrokerManagerDep, TelegramBotsServiceDep, ConnManagerDep, UowDep, MessageServiceDep
from src.core.exceptions.bots import WebhookCreateMessageError
from loguru import logger

webhook = APIRouter(prefix="/webhooks", tags=["Telegram Live Receive"])

@webhook.post("/{bot_id}/telegram")
async def receive_telegram_message(
    request: Request, 
    tg_bot_service: TelegramBotsServiceDep,
    m_service: MessageServiceDep,
    broker: BrokerManagerDep,
    conn_manager: ConnManagerDep,
    uow: UowDep,
    bot_id: int = Path(...),
):
    payload = await request.json()
    try:
        await tg_bot_service.save_message(payload, bot_id, uow, m_service, broker, conn_manager)
        return {"status": "success", "message": "delivered"}
    except Exception as e:
        logger.exception(f"CRITICAL: Failed to process telegram message for bot {bot_id}. Error: {e}")
        raise WebhookCreateMessageError()
    
