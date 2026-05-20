from fastapi import APIRouter, Path, Request
from src.api.dependecies import TelegramBotsServiceDep, UowDep
from loguru import logger


router = APIRouter(prefix="/webhooks", tags=["Telegram Live Receive"])

@router.post("/{bot_id}/telegram")
async def receive_telegram_message(
    request: Request, 
    tg_bot_service: TelegramBotsServiceDep,
    uow: UowDep,
    bot_id: int = Path(..., description="ID бота, которому предназначено сообщение"),
):
    pyload = await request.json()
    await tg_bot_service.save_message(pyload, bot_id, uow)
    return {"status": "success", "message": "delivered"}
    
