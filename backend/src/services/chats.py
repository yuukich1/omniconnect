from .uow import IUnitOfWork

class ChatService:
    
    async def list_by_user_id(self, user_id: int, uow: IUnitOfWork):
        async with uow:
            chats = await uow.chats.list_by_user_id(user_id)
            return chats