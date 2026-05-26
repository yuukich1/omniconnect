

from sqlalchemy import select

from src.models.post import Post, PostAttachment

from .base import SQLAlchemyRepository


class PostRepository(SQLAlchemyRepository):
    
    model = Post
    
    async def list_by_user_id(self, user_id: int):
        query = select(self.model).join(Post).filter(Post.owner_id == user_id)
        result = await self.session.execute(query)
        return result.scalars().all()
    
class PostAttachmentRepository(SQLAlchemyRepository):
    
    model = PostAttachment
    
    async def get_by_post_id(self, post_id: int):
        query = select(self.model).filter(PostAttachment.post_id == post_id)
        result = await self.session.execute(query)
        return result.scalars().all()
    
    