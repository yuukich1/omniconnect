from fastapi import APIRouter
from src.schemas.users import UserRegister
from .dependecies import UowDep, UsersServiceDep

router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post('/register')
async def register(data: UserRegister, u_service: UsersServiceDep, uow: UowDep):
    user = await u_service.register(data, uow)
    return {"status": "ok", "user_id": user.id}