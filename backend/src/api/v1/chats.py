from fastapi import APIRouter
from src.api.dependecies import UowDep, CurrentUserDep


router = APIRouter(prefix='/chats', tags=['Chats'])

@router.get('/')
async def list_chats(uow: UowDep, user: CurrentUserDep):
    async with uow:
        chats = await uow.chats.list_by_user_id(user.id)
        return chats

