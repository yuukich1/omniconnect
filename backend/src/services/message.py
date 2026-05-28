from typing import Dict, Optional
import uuid
from fastapi.encoders import jsonable_encoder
from .uow import IUnitOfWork
from src.schemas.auth import CurrentUser
from src.models import Message
from .connect_manager import ConnectionManager
from src.core.config import settings
from src.schemas.message import MessageResponse

class MessageService:
    
    async def handle_message(self, chat_id: uuid.UUID, user: CurrentUser, uow: IUnitOfWork, conn_manager: ConnectionManager,
                            text: Optional[str] = None, attachemts: Optional[Dict] = None):
        async with uow: 
            chat = await uow.chat.get(chat_id)
            if not chat:
                return await self._send_error(chat_id=chat_id, code='NOT FOUND', message='Chat not found', conn_manager=conn_manager)
            members = await uow.chat_members.get_members_by_chat(chat_id)
            if user.id not in [member.user_id for member in members]:
                return await self._send_error(chat_id=chat_id, code='FORBIDDEN', message='You are not member', conn_manager=conn_manager)
            message_model = await uow.message.create(Message(
                chat_id=chat_id,
                author_id=user.id,
                sender_metadata={
                    'display_name': user.username,
                    'is_bot': False,
                    'api_version': settings.api_version,
                },
                text=text,
                media=attachemts
            ))
            await uow.commit()
            message_dict = MessageResponse.model_validate(message_model, from_attributes=True).model_dump()
            message_json = jsonable_encoder(message_dict)
            await conn_manager.broadcast(chat_id, message_json)            
            
    
    async def _send_error(self, chat_id: uuid.UUID, code: str, message: str, conn_manager: ConnectionManager):
        message_error = {'type': 'ERROR', 'payload': { 'code': code, 'message': message } }
        await conn_manager.broadcast(chat_id, message_error)