from typing import List, Optional

from fastapi import APIRouter, File, Form, Query, UploadFile
from src.api.dependecies import TelegramBotsServiceDep, UowDep, CurrentUserDep, MessageServiceDep

router = APIRouter(prefix='/messages', tags=['Messages'])


@router.get('/{chat_id}')
async def get_messages(chat_id: int, m_service: MessageServiceDep, uow: UowDep, user: CurrentUserDep, show: int = Query(50)):
    messages = await m_service.get_messages(chat_id, user.id, show, uow)
    return messages

@router.post('/{chat_id}/send')
async def send_message(chat_id: int, 
                       uow: UowDep, 
                       t_service: TelegramBotsServiceDep, 
                       user: CurrentUserDep, 
                       text: Optional[str] = Form(None), 
                       attachments: Optional[UploadFile] = File(None)):
    await t_service.send_message(chat_id, text, attachments, user, uow)
    return {"status": "ok"}