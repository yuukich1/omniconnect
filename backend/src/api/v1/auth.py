from fastapi import APIRouter, Body, Form
from src.schemas.users import UserRegister, RefreshTokenBody
from src.api.dependecies import UowDep, AuthServiceDep

router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post('/register')
async def register(data: UserRegister, a_service: AuthServiceDep, uow: UowDep):
    user = await a_service.register(data, uow)
    return {"status": "ok", "user_id": user.id}


@router.post('/token')
async def login(a_service: AuthServiceDep, uow: UowDep, username: str = Form(...), password: str = Form(...)):
    tokens = await a_service.login(username, password, uow)
    return tokens


@router.post('/refresh')
async def refresh_token(a_service: AuthServiceDep, uow: UowDep, grant_type: str = Form(...), refresh_token: str = Form(...)): 
    token = await a_service.refresh_token(refresh_token, uow)
    return token


@router.delete('/exit')
async def exit(data: RefreshTokenBody, a_service: AuthServiceDep, uow: UowDep):
    await a_service.exit(data.refresh_token, uow)
    return {'status': 'ok'}
    