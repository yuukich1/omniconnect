from typing import List

from fastapi import APIRouter
from src.api.dependencies.service import ChatServiceDependency
from src.api.dependencies.connect import UnitOfWorkDependency
from src.api.dependencies.auth import CurrentUserDependency
from src.schemas.chats import ChatCreateRequest, ChatDTO
from src.schemas import CreateBaseResponse

router = APIRouter(prefix='/chats', tags=['chats'])

@router.post('/', status_code=201, response_model=CreateBaseResponse)
async def create_chat(chat_data: ChatCreateRequest, owner: CurrentUserDependency, ch_service: ChatServiceDependency, uow: UnitOfWorkDependency):
    chat = await ch_service.create_chat(chat_data, owner, uow)
    return {'id': chat.id}

@router.get('/', response_model=List[ChatDTO])
async def get_chats(user: CurrentUserDependency, ch_service: ChatServiceDependency, uow: UnitOfWorkDependency):
    chats = await ch_service.get_chats_by_user(user, uow)
    return chats