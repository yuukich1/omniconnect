from typing import List, Optional, Union
import uuid
from fastapi import APIRouter, Query
from src.api.dependencies.auth import CurrentUserDependency
from src.schemas.users import UserUpdateRequest
from src.api.dependencies.service import UserServiceDependency
from src.api.dependencies.connect import UnitOfWorkDependency
from src.schemas.users import UserResponse

router = APIRouter(prefix="/users", tags=["users"])



@router.get('/', response_model=Union[UserResponse, List[UserResponse]])
async def get_users(u_service: UserServiceDependency, uow: UnitOfWorkDependency, username: Optional[str] = Query(None)):
    users = await u_service.get_user_by_username(username, uow) if username else await u_service.get_list_user(uow)
    return users
    

@router.get('/{user_id}', response_model=UserResponse)
async def get_user_by_id(user_id: str, u_service: UserServiceDependency, uow: UnitOfWorkDependency):
    return await u_service.get_user_by_id(uuid.UUID(user_id), uow)


@router.patch('/{user_id}', response_model=UserResponse)
async def update_user(user_id: str, update_data: UserUpdateRequest, current_user: CurrentUserDependency, u_service: UserServiceDependency, uow: UnitOfWorkDependency):
    return await u_service.update_user(update_data=update_data, current_user=current_user, uow=uow, user_id=uuid.UUID(user_id))