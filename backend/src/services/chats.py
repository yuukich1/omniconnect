from typing import List

from src.schemas.auth import CurrentUser
from .uow import IUnitOfWork
from src.models import Chat, ChatMembers
from src.enum import chats as ch_enum
from src.schemas.chats import ChatCreateRequest, ChatDTO, UserShortDTO
from src.api.exceptions import exceptions as exc

class ChatService:
    
    async def create_chat(self, chat_data: ChatCreateRequest, owner: CurrentUser, uow: IUnitOfWork):
        async with uow:
            chat = await uow.chat.create(Chat(owner_id=owner.id, type=chat_data.type.value))
            await uow.chat_members.create(ChatMembers(chat_id=chat.id, user_id=owner.id, role=ch_enum.MemberRole.OWNER.value))
            if chat_data.member_id:
                if chat_data.member_id == owner.id:
                    raise exc.DataIntegrityError
                member = await uow.users.get(chat_data.member_id)
                if not member:
                    raise exc.NotFoundError('Member not found')
                await uow.chat_members.create(ChatMembers(
                    chat_id=chat.id, 
                    user_id=chat_data.member_id, 
                    role=ch_enum.MemberRole.MEMBER.value
                ))
            await uow.commit()
            return chat
        
    async def get_chats_by_user(self, user: CurrentUser, uow: IUnitOfWork):
        async with uow:
            result = await uow.chat.get_list_user_chat(user.id)
            return self._map_chat_to_dto(result)
        
    def _map_chat_to_dto(self, rows: List):
        chats_map = {}
        for chat, user in rows:
            if chat.id not in chats_map:
                chats_map[chat.id] = {
                    'id': chat.id,
                    'type': chat.type,
                    'created_at': chat.created_at,
                    'members': []
                }
            member = UserShortDTO(id=user.id, username=user.username)
            chats_map[chat.id]['members'].append(member)
            
        return [ChatDTO(**data) for data in chats_map.values()]
        
    
