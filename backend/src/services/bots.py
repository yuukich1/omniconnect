from src.schemas.users import CurrentUser
from src.core.exceptions.bots import BotNotFoundError
from .uow import IUnitOfWork
from src.schemas.bots import BotCreateRequest
import aiogram as tg
from src.core.config import session_tg_bot, settings
class BotsService: 
    
    async def create_bot(self, bot_data: BotCreateRequest, user_id: int, uow: IUnitOfWork):
        bot_dict = bot_data.model_dump()
        bot_dict['user_id'] = user_id
        async with uow:
            bot = await uow.bots.save(bot_dict)
            await uow.commit()
            if bot_data.platform == 'telegram':
                await tg.Bot(token=bot.token, session=session_tg_bot).set_webhook(f"{settings.DOMAIN}/webhooks/{bot.id}/telegram")
            return bot
        
    async def list_bots(self, user_id: int, uow: IUnitOfWork):
        async with uow:
            bots = await uow.bots.list_by_user_id(user_id)
            return bots
        
    async def get_bot(self, bot_id: int, user_id: int, uow: IUnitOfWork):
        async with uow:
            bot = await uow.bots.get(bot_id)
            if bot is None or bot.user_id != user_id:
                raise BotNotFoundError(bot_id)
            return bot
        
    async def update_bot(self, bot_id: int, token: str, user_id: int, uow: IUnitOfWork):
        async with uow:
            bot = await uow.bots.get(bot_id)
            if bot is None or bot.user_id != user_id:
                raise BotNotFoundError(bot_id)
            await uow.bots.update(bot_id, {"token": token})
            await uow.commit()
            return bot
        
    async def delete_bot(self, bot_id: int, user: CurrentUser, uow: IUnitOfWork):
        async with uow:
            bot = await uow.bots.get(bot_id)
            if not bot or bot.user_id != user.id or user.role != 'admin':
                raise BotNotFoundError(bot_id)
            await uow.bots.delete(bot_id)
            await uow.commit()
            return bot
