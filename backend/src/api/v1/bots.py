from typing import List

from fastapi import APIRouter

from src.schemas.bots import BotCreateRequest, BotResponse, UpdateTokenRequest
from src.api.dependecies import UowDep, BotsServiceDep, CurrentUserDep


router = APIRouter(prefix='/bots', tags=['Bots'])

@router.post('/')
async def create_bot(bot_data: BotCreateRequest, b_service: BotsServiceDep, uow: UowDep, user: CurrentUserDep):
    bot = await b_service.create_bot(bot_data, user.id, uow)
    return {"status": "ok", "bot_id": bot.id}

@router.get('/', response_model=List[BotResponse])
async def list_bots(b_service: BotsServiceDep, uow: UowDep, user: CurrentUserDep):
    bots = await b_service.list_bots(user.id, uow)
    return bots

@router.get('/{bot_id}', response_model=BotResponse)
async def get_bot(bot_id: int, b_service: BotsServiceDep, uow: UowDep, user: CurrentUserDep):
    bot = await b_service.get_bot(bot_id, user.id, uow)
    return bot

@router.put('/{bot_id}')
async def update_bot(bot_id: int, token_data: UpdateTokenRequest, b_service: BotsServiceDep, uow: UowDep, user: CurrentUserDep):
    bot = await b_service.update_bot(bot_id, token_data.token, user.id, uow)
    return {"status": "ok", "bot_id": bot.id}

@router.delete('/{bot_id}')
async def delete_bot(bot_id: int, b_service: BotsServiceDep, uow: UowDep, user: CurrentUserDep):
    await b_service.delete_bot(bot_id, user, uow)