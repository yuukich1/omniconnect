from typing import List

from fastapi import APIRouter

from src.schemas.bots import BotCreateRequest, BotResponse
from src.api.dependecies import UowDep, BotsServiceDep, CurrentUserDep


router = APIRouter(prefix='/bots', tags=['Bots'])

@router.post('/')
async def create_bot(bot_data: BotCreateRequest, b_service: BotsServiceDep, uow: UowDep, user_id: CurrentUserDep):
    bot = await b_service.create_bot(bot_data, user_id, uow)
    return {"status": "ok", "bot_id": bot.id}

@router.get('/', response_model=List[BotResponse])
async def list_bots(b_service: BotsServiceDep, uow: UowDep, user_id: CurrentUserDep):
    bots = await b_service.list_bots(user_id, uow)
    return bots

@router.get('/{bot_id}', response_model=BotResponse)
async def get_bot(bot_id: int, b_service: BotsServiceDep, uow: UowDep, user_id: CurrentUserDep):
    bot = await b_service.get_bot(bot_id, user_id, uow)
    return bot

