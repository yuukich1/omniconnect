from fastapi import APIRouter, Form
from src.schemas.users import UserRegister
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

