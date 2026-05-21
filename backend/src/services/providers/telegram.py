
import os
from typing import Optional
import httpx
import aiogram as tg
from src.schemas.users import CurrentUser
from src.core.exceptions.bots import BotNotFoundError, BotPermissionError
from src.core.exceptions.chats import ChatNotFoundError
from src.services import IUnitOfWork
from .base import IPlatformBotsService
from src.schemas.bots import TelegramMessageDTO

class TelegramBotsService(IPlatformBotsService):
    
    upload_dir = "uploads/telegram"
    
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

    def _save_file_to_disk(self, content: bytes, file_id: str, bot_id: int, tg_file_path: str) -> str:
        _, ext = os.path.splitext(tg_file_path)
        local_filename = f"bot_{bot_id}_{file_id[-12:]}{ext}"
        local_path = os.path.join(self.upload_dir, local_filename)
        os.makedirs(self.upload_dir, exist_ok=True)
        with open(local_path, "wb") as f:
            f.write(content)
        return local_path

    async def _download_telegram_file(self, file_id: str, bot_id: int, token: str) -> Optional[str]:
        try:
            async with httpx.AsyncClient() as client:
                tg_file_path = await self._get_telegram_file_path(client, file_id, token)
                if not tg_file_path:
                    return None

                file_content = await self._download_file_bytes(client, tg_file_path, token)
                if not file_content:
                    return None

                return self._save_file_to_disk(file_content, file_id, bot_id, tg_file_path)
        except Exception as e:
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
        
    async def send_message(self, chat_id: int, text: str, user: CurrentUser, uow: IUnitOfWork):
        async with uow:
            bots_from_db = await uow.bots.get_chat_id(chat_id)
            if bots_from_db is None:
                raise ChatNotFoundError(chat_id)
            if bots_from_db.user_id != user.id:
                raise BotPermissionError
            chat = await uow.chats.get(chat_id)
            if chat is None:
                raise ChatNotFoundError(chat_id)
            bot = tg.Bot(token=bots_from_db.token)
            if await bot.send_message(chat_id=chat.chat_id, text=text):
                message_dict = {
                    "chat_id": chat_id,
                    "text": text,
                    "username": user.username
                }
                await uow.message.save(message_dict)
            