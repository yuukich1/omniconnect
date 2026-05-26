from typing import List

from fastapi import APIRouter, Body, File, UploadFile
from src.api.dependecies import UowDep, CurrentUserDep, PostServiceDep

router = APIRouter(prefix='/posts', tags=['Posts'])

@router.post('/')
async def create_post(user: CurrentUserDep, p_service: PostServiceDep, uow: UowDep, content: str = Body(...), attachments: List[UploadFile] = File(None)):
    post = await p_service.create_post(content, attachments, user, uow)
    return {'status': 'ok', 'id': post.id}

@router.get('/')
async def list_posts(p_service: PostServiceDep, uow: UowDep):
    posts = await p_service.list_posts(uow)
    return posts

@router.get('/me')
async def list_me_posts(user: CurrentUserDep, p_service: PostServiceDep, uow: UowDep):
    posts = await p_service.list_user_posts(user.id, uow)
    return posts

@router.get('/user/{user_id}')
async def list_user_posts(user_id: int, p_service: PostServiceDep, uow: UowDep):
    posts = await p_service.list_user_posts(user_id, uow)
    return posts