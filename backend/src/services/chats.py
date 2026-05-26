from src.schemas.users import CurrentUser
from src.schemas.chats import Chat
from src.core.exceptions.auth import UserNotFoundError, CoflitUserError
from .uow import IUnitOfWork

class ChatService:
    
    async def list_by_user_id(self, user: CurrentUser, uow: IUnitOfWork):
        async with uow:
            chats = await uow.chats.list_by_user_id(user.id)
            response = []
            for chat in chats:
                chat_schema = Chat.model_validate(chat, from_attributes=True)
                if chat.owner_id != user.id:
                    owner = await uow.users.get(chat.owner_id)
                    if owner:
                        chat_schema.username = owner.username
                response.append(chat_schema)
            return response
        
    async def create_chat(self, member_id: int, user: CurrentUser, uow: IUnitOfWork):
        if member_id == user.id:
            raise CoflitUserError
        async with uow:
            member = await uow.users.get(member_id)
            if not member:
                raise UserNotFoundError()
            chat = await uow.chats.save({
                'owner_id': user.id,
                'member_id': member.id,
                'username': member.username
            })
            await uow.commit()
            return chat