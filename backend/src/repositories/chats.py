from typing import List
import uuid

from sqlalchemy import select
from src.models import Chat, ChatMembers, User
from .base import SqlAclehmyRepository

class ChatsRepository(SqlAclehmyRepository):
    
    model = Chat
    
    async def get_list_user_chat(self, user_id: uuid.UUID):
        subquery = select(ChatMembers.chat_id).filter(ChatMembers.user_id == user_id)
        query = select(Chat, User) \
                .join(ChatMembers, Chat.id == ChatMembers.chat_id) \
                .join(User, ChatMembers.user_id == User.id) \
                .filter(ChatMembers.user_id != user_id) \
                .filter(Chat.id.in_(subquery))
                
        result = await self.session.execute(query)
        return list(result.all())
    
class ChatMembersRepository(SqlAclehmyRepository):
    
    model = ChatMembers
    
    async def get_members_by_chat(self, chat_id: uuid.UUID) -> List[ChatMembers]:
        query = select(ChatMembers).filter(ChatMembers.chat_id == chat_id)
        result = await self.session.execute(query)
        return list(result.scalars().all())