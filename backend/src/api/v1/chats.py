from fastapi import APIRouter
from src.api.dependecies import UowDep, CurrentUserDep, ChatServiceDep


router = APIRouter(prefix='/chats', tags=['Chats'])

@router.get('/')
async def list_chats(ch_service: ChatServiceDep, uow: UowDep, user: CurrentUserDep):
    return await ch_service.list_by_user_id(user, uow)

@router.post('/{member_id}')
async def create_chat(member_id: int, ch_service: ChatServiceDep, user: CurrentUserDep, uow: UowDep):
    chat = await ch_service.create_chat(member_id, user, uow)
    return {'status': 'ok', 'id': chat.id}