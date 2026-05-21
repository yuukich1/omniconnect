
import mimetypes
from typing import Optional
from fastapi import UploadFile
import httpx
import aiogram as tg
from src.schemas.users import CurrentUser
from src.core.exceptions.bots import BotNotFoundError, BotPermissionError
from src.core.exceptions.chats import ChatNotFoundError
from src.services import IUnitOfWork
from .base import IPlatformBotsService
from src.schemas.bots import TelegramMessageDTO
import src.utils as util
from src.core.config import session_tg_bot

class TelegramBotsService(IPlatformBotsService):
    

    
    async def _extract_message_data(self, payload: dict) -> TelegramMessageDTO:
        
        message = payload.get("message", {})
        chat = message.get("from", {})
        
        media_field = next((message.get(k) for k in ("document", "voice", "video", "animation", "audio") if message.get(k)), None)
        file_id = media_field.get("file_id") if media_field else (message.get("photo")[-1].get("file_id") if message.get("photo") else None)

        return TelegramMessageDTO(
            chat_id=chat.get("id", "unknown"),
            username=chat.get("username", "unknown"),
            text=message.get("text") or message.get("caption"),
            file_id=file_id,
            file_name="unknown_file",
            media_type="media" if file_id else "text"
        )
        
    async def _get_telegram_file_path(self, client: httpx.AsyncClient, file_id: str, token: str) -> Optional[str]:
        response = await client.post(
            f"https://api.telegram.org/bot{token}/getFile", 
            json={"file_id": file_id}
        )
        file_info = response.json()
        return file_info["result"]["file_path"] if file_info.get("ok") else None

    async def _download_file_bytes(self, client: httpx.AsyncClient, tg_file_path: str, token: str) -> Optional[bytes]:
        download_url = f"https://api.telegram.org/file/bot{token}/{tg_file_path}"
        response = await client.get(download_url)
        return response.content if response.status_code == 200 else None

   

    async def _download_telegram_file(self, file_id: str, bot_id: int, token: str) -> Optional[str]:
        try:
            async with httpx.AsyncClient() as client:
                tg_file_path = await self._get_telegram_file_path(client, file_id, token)
                if not tg_file_path:
                    return None

                file_content = await self._download_file_bytes(client, tg_file_path, token)
                if not file_content:
                    return None

                return await util.save_file_to_disk(file_content, tg_file_path, bot_id)
        except Exception:
            return None
        
    async def save_message(self, payload: dict, bot_id: int, uow: IUnitOfWork):
        message_data = await self._extract_message_data(payload)
        async with uow:
            bot = await uow.bots.get(bot_id)
            if bot is None:
                raise BotNotFoundError(bot_id)
            local_file_path = None
            if message_data.file_id:
                local_file_path = await self._download_telegram_file(
                    file_id=message_data.file_id,
                    bot_id=bot_id,
                    token=bot.token
                )
            chat = await uow.chats.get_by_chat_id_and_bot_id(message_data.chat_id, bot_id)
            if chat is None:
                chat_dict = {
                    "chat_id": message_data.chat_id,
                    "username": message_data.username,
                    "bot_id": bot_id
                }
                chat = await uow.chats.save(chat_dict)

            message_dict = {
                "chat_id": chat.id, 
                "text": message_data.text,
                'username': message_data.username,
                "attachments_url": local_file_path 
            }
            await uow.message.save(message_dict)
            await uow.commit()
            return message_dict
        
    async def send_message(self, chat_id: int, text: Optional[str], attachments: Optional[UploadFile], user: CurrentUser, uow: IUnitOfWork):
        local_file_path = None
        async with uow:
            bots_from_db = await uow.bots.get_chat_id(chat_id)
            if bots_from_db is None:
                raise ChatNotFoundError(chat_id)
            if bots_from_db.user_id != user.id:
                raise BotPermissionError
            chat = await uow.chats.get(chat_id)
            if chat is None:
                raise ChatNotFoundError(chat_id)
            bot = tg.Bot(token=bots_from_db.token, session=session_tg_bot)
            if attachments:
                local_file_path = await self._send_attachments(bot, chat.chat_id, attachments, text, bots_from_db.id)
            elif text:
                await bot.send_message(chat.chat_id, text)
            else:
                raise ValueError("Сообщение не может быть пустым")

            message_dict = {
                "chat_id": chat.id, 
                "text": text,
                "username": user.username,
                "attachments_url": local_file_path 
            }
            await uow.message.save(message_dict)
                
    async def _send_attachments(self, bot: tg.Bot, chat_id: int, attachments: UploadFile, text: Optional[str], owner_id: int):
        file_content = await attachments.read()
        filename = attachments.filename or "unknown_file"
        filepath = await util.save_file_to_disk(file_content, original_filename=filename, owner_id=owner_id)
        
        mime_type, _ = mimetypes.guess_type(filename)
        
        try:
            if mime_type and mime_type.startswith('image/'):
                await bot.send_photo(chat_id=chat_id, photo=tg.types.FSInputFile(filepath), caption=text)
                
            elif mime_type and mime_type.startswith('video/'):
                await bot.send_video(chat_id=chat_id, video=tg.types.FSInputFile(filepath), caption=text)
                
            elif mime_type and mime_type.startswith('audio/'):
                await bot.send_audio(chat_id=chat_id, audio=tg.types.FSInputFile(filepath), caption=text)
                
            else:
                await bot.send_document(chat_id=chat_id, document=tg.types.FSInputFile(filepath), caption=text)
                
        except Exception as e:
            print(f"Ошибка при отправке файла: {e}")
            raise
        return filepath
                    
            