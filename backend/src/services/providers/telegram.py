import mimetypes
import os
from typing import List, Optional
from fastapi import UploadFile
import httpx
import aiogram as tg
from aiogram.utils.media_group import MediaGroupBuilder
from src.schemas.users import CurrentUser
from src.core.exceptions.bots import BotNotFoundError, BotPermissionError
from src.core.exceptions.chats import ChatNotFoundError
from src.services import IUnitOfWork
from .base import IPlatformBotsService
from src.schemas.bots import TelegramMessageDTO
import src.utils as util
from src.core.config import session_tg_bot, settings

class TelegramBotsService(IPlatformBotsService):
    def __init__(self):
        self.client = httpx.AsyncClient()

    def _extract_message_data(self, payload: dict) -> TelegramMessageDTO:
        message = payload.get("message", {})
        chat = message.get("from", {})
        
        text = message.get("text") or message.get("caption")
        media_field = next((message.get(k) for k in ("document", "voice", "video", "animation", "audio") if message.get(k)), None)
        
        if message.get("photo"):
            file_id = message.get("photo")[-1].get("file_id")
        else:
            file_id = media_field.get("file_id") if media_field else None

        return TelegramMessageDTO(
            chat_id=int(chat.get("id")),
            username=chat.get("username", "unknown"),
            text=text,
            file_id=file_id,
            file_ids=[file_id] if file_id else [],
            media_group_id=message.get("media_group_id"),
            file_name=media_field.get("file_name") if media_field and "file_name" in media_field else "unknown_file",
            media_type="media" if file_id else "text"
        )
            
    async def _get_telegram_file_path(self, client: httpx.AsyncClient, file_id: str, token: str) -> Optional[str]:
        response = await client.get(f"https://api.telegram.org/bot{token}/getFile", params={"file_id": file_id})
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
                if not tg_file_path: return None
                file_content = await self._download_file_bytes(client, tg_file_path, token)
                if not file_content: return None
                return await util.save_file_to_disk(file_content, tg_file_path, bot_id, 'telegram')
        except Exception as e:
            print(f"Error downloading file {file_id}: {e}")
            return None
        
    async def save_message(self, payload: dict, bot_id: int, uow: IUnitOfWork):
        msg_data = self._extract_message_data(payload)
        async with uow:
            db_bot = await self._bot_exist(uow, bot_id=bot_id)
            chat = await self._get_or_create_chat(uow, msg_data, db_bot.id)
            message = await self._get_or_create_message(uow, msg_data, chat.id)
            if msg_data.file_id:
                await self._process_attachment(uow, message.id, msg_data.file_id, db_bot)
            await uow.commit()
            return msg_data

    async def _get_or_create_chat(self, uow, data, bot):
        chat = await uow.chats.get_by_chat_id_and_bot_id(data.chat_id, bot.id)
        return chat or await uow.chats.save({
            'chat_external_id': data.chat_id, 
            'username': data.username, 
            'bot_id': bot.id,
            'owner_id': bot.user_id
        })

    async def _get_or_create_message(self, uow, data, chat_id):
        if data.media_group_id:
            message = await uow.message.get_by_media_group(data.media_group_id)
            if message:
                if data.text and not message.text:
                    await uow.message.update_text(message.id, data.text)
                return message
        return await uow.message.save({
            'chat_id': chat_id,
            'text': data.text,
            'media_group_id': data.media_group_id,
            'is_from_bot': False,
            'username': data.username
        })

    async def _process_attachment(self, uow, message_id, file_id, db_bot):
        filename = await self._download_telegram_file(file_id, db_bot.id, db_bot.token)
        if filename:
            attachment = await uow.attachments.save({'path': filename})
            await uow.message_attachemnts.save({
                'message_id': message_id, 
                'attachments_id': attachment.id
            })
            
    async def _bot_exist(self, uow, bot_id: Optional[int] = None, chat_id: Optional[int] = None):
        bot = await uow.bots.get(bot_id) if bot_id else await uow.bots.get_chat_id(chat_id)
        if not bot: raise BotNotFoundError()
        return bot
            
    async def send_message(self, chat_id: int, text: Optional[str], attachments: Optional[List[UploadFile]], user: CurrentUser, uow: IUnitOfWork):
        async with uow:
            db_bot = await self._bot_exist(uow, chat_id=chat_id)
            if db_bot.user_id != user.id: raise BotPermissionError(db_bot.id)
            chat = await uow.chats.get(chat_id)
            if not chat: raise ChatNotFoundError(chat_id)
            tg_bot = tg.Bot(token=db_bot.token, session=session_tg_bot)
            message = await uow.message.save({
                'chat_id': chat.id,
                'text': text,
                'is_from_bot': True,
                'username': user.username
            })
            if attachments:
                list_local_filepath = await self._send_attachments(tg_bot, chat.chat_external_id, attachments, text, db_bot.id)
                for path in list_local_filepath:
                    attachment = await uow.attachments.save({"path": path})
                    await uow.message_attachemnts.save({
                        "message_id": message.id,
                        "attachments_id": attachment.id
                    })
            else:
                await tg_bot.send_message(chat_id=chat.chat_external_id, text=text or "")
            await uow.commit()
            return

    async def _send_attachments(self, tg_bot: tg.Bot, chat_id: int, attachments: List[UploadFile], text: Optional[str], owner_id: int):
        list_filenames = []
        
        for file in attachments:
            file_content = await file.read()
            filename = file.filename or 'unknown_file'
            name = await util.save_file_to_disk(file_content, filename, owner_id, 'telegram')
            list_filenames.append(name)
            
        media_group = MediaGroupBuilder(caption=text)
        
        for name in list_filenames:
            full_path = os.path.join(settings.UPLOAD_DIR, name)
            
            mime_type, _ = mimetypes.guess_type(name)
            input_file = tg.types.FSInputFile(full_path)
            
            if mime_type and mime_type.startswith('image/'): media_group.add_photo(media=input_file)
            elif mime_type and mime_type.startswith('video/'): media_group.add_video(media=input_file)
            elif mime_type and mime_type.startswith('audio/'): media_group.add_audio(media=input_file)
            else: media_group.add_document(media=input_file)
        
        await tg_bot.send_media_group(chat_id=chat_id, media=media_group.build()) # type: ignore
        return list_filenames