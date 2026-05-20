from fastapi import APIRouter, Form
from src.api.dependecies import UowDep, TelegramBotsServiceDep, CurrentUserDep


router = APIRouter(prefix='/chats', tags=['Chats'])

@router.get('/')
async def list_chats(uow: UowDep, user_id: CurrentUserDep):
    async with uow:
        chats = await uow.chats.list_by_user_id(user_id)
        return chats

@router.post('/{chat_id}/send')
async def send_message(chat_id: int, uow: UowDep, t_service: TelegramBotsServiceDep, user_id: CurrentUserDep, text: str = Form(...)):
    await t_service.send_message(chat_id, text, user_id, uow)
    return {"status": "ok"}