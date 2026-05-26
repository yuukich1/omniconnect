


from typing import List

from fastapi import UploadFile

from src.schemas.users import CurrentUser
from src.services.uow import IUnitOfWork
from src.utils.file import save_file_to_disk

class PostService:
    
    async def create_post(self, content: str, attachments: List[UploadFile], user: CurrentUser, uow: IUnitOfWork):
        async with uow:
            post_dict = {
                'owner_id': user.id,
                'content': content
            }
            post = await uow.post.save(post_dict)
            await uow.commit()
            
            for file in attachments:
                file_path = await save_file_to_disk( await file.read(), file.filename, user.id, subfolder='posts') # type: ignore
                post_attachment_dict = {
                    'post_id': post.id,
                    'file_path': file_path
                }
                await uow.post_attachment.save(post_attachment_dict)
            
            await uow.commit()
            return post
    
    
    async def list_posts(self, uow: IUnitOfWork):
        response = []
        async with uow:
            posts = await uow.post.get_list()
            for post in posts:
                attachments = await uow.post_attachment.get_by_post_id(post.id)
                response.append({
                    'id': post.id,
                    'owner_id': post.owner_id,
                    'content': post.content,
                    'attachments': [f'/static/{att.file_path}' for att in attachments],
                    'created_at': post.created_at.isoformat()
                })
            return response
    
    async def list_user_posts(self, user_id: int, uow: IUnitOfWork):
        response = []
        async with uow:
            posts = await uow.post.list_by_user_id(user_id)
            for post in posts:
                attachments = await uow.post_attachment.get_by_post_id(post.id)
                response.append({
                    'id': post.id,
                    'owner_id': post.owner_id,
                    'content': post.content,
                    'attachments': [f'/static/{att.file_path}' for att in attachments],
                    'created_at': post.created_at.isoformat()
                })
            return response