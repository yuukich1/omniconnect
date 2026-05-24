from fastapi import APIRouter, Path, Request
from src.api.dependecies import TelegramBotsServiceDep, UowDep
from src.core.exceptions.bots import WebhookCreateMessageError
from loguru import logger

router = APIRouter(prefix="/webhooks", tags=["Telegram Live Receive"])

@router.post("/{bot_id}/telegram")
async def receive_telegram_message(
    request: Request, 
    tg_bot_service: TelegramBotsServiceDep,
    uow: UowDep,
    bot_id: int = Path(...),
):
    payload = await request.json()
    try:
        await tg_bot_service.save_message(payload, bot_id, uow)
        return {"status": "success", "message": "delivered"}
    except Exception as e:
        logger.exception(f"CRITICAL: Failed to process telegram message for bot {bot_id}. Error: {e}")
        raise WebhookCreateMessageError()
    
