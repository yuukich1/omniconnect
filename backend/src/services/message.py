

from backend.src.services.uow import IUnitOfWork
from src.core.exceptions.chats import ChatNotFoundError

class MessageService:
    
    async def get_messages(self, chat_id: int, user_id: int, show: int, uow: IUnitOfWork):
        async with uow:
            chat = await uow.chats.get(chat_id)
            if chat_id is None and chat.bot.user_id != user_id:
                raise ChatNotFoundError(chat_id)
            messages = await uow.message.get_messages_by_chat_id(chat_id, show)
            return messages