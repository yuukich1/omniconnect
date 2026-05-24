

from backend.src.services.uow import IUnitOfWork
from src.core.exceptions.chats import ChatNotFoundError

class MessageService:
    
    async def get_messages(self, chat_id: int, user_id: int, show: int, uow: IUnitOfWork):
        async with uow:
            chat = await uow.chats.get(chat_id)
            if not chat:
                raise ChatNotFoundError(chat_id)
            
            messages = await uow.message.get_messages_with_attachments_by_chat_id(chat_id, show)

            return [
                {
                    "id": msg.id,
                    "text": msg.text,
                    "is_from_bot": msg.is_from_bot,
                    "created_at": msg.created_at,
                    "files": [
                        f"/static/{att.path.replace(chr(92), '/')}" 
                        for att in msg.attachments
                    ]
                }
                for msg in messages
            ]