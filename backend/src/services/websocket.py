
from typing import Optional

from fastapi import WebSocketException, status
from fastapi.encoders import jsonable_encoder
from src.services.message import MessageService
from src.schemas.users import CurrentUser
from src.schemas.message import MessageSchema
from .uow import IUnitOfWork
from .redis_manager import RedisMessageBroker
from .providers.telegram import TelegramBotsService
from .connect_manager import ConnectionManager

class WebsocketManager:
    async def handle_message(
        self, 
        text: Optional[str], 
        chat_id: int, 
        user: CurrentUser, 
        uow: IUnitOfWork, 
        broker: RedisMessageBroker, 
        tg_service: TelegramBotsService,
        conn_manager: ConnectionManager,
        m_service: MessageService
    ):
        async with uow:
            chat = await uow.chats.get(chat_id)
            if not chat or (chat.owner_id != user.id and chat.member_id != user.id):
                raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
            if not chat.bot_id:
                pass 
            else:
                bot = await uow.bots.get(chat.bot_id)
                if not bot or bot.user_id != user.id:
                    raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)

                if bot.platform == 'telegram':
                    await tg_service.send_message(
                        chat_id=chat_id, text=text, attachments=None, user=user, uow=uow, m_service=m_service, broker=broker, conn_manager=conn_manager
                    )
                    return

            message_model = await uow.message.save({
                'chat_id': chat_id,
                'text': text,
                'username': user.username
            })
            await uow.commit()
            message_data = MessageSchema.model_validate(await m_service.get_message_by_id(message_model.id, uow), from_attributes=True).model_dump()
            message_data = jsonable_encoder(message_model)
            await broker.publish(str(chat_id), message_data)
            
            await conn_manager.broadcast(chat_id, message_data)