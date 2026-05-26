from fastapi import APIRouter, Query
from src.api.dependecies import UserServiceDep, UowDep

router = APIRouter(prefix='/users', tags=['Users'])

@router.get('/')
async def get_users_by_username(u_service: UserServiceDep, uow: UowDep, username: str = Query(...)):
    user = await u_service.get_by_username(username, uow)
    if user:
        return {"id": user.id, "username": user.username}
    return {"error": "User not found"}