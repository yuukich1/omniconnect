import uuid

from fastapi import APIRouter
from src.api.dependencies.auth import CurrentUserDependency
from src.schemas.users import UserUpdateRequest
from src.api.dependencies.service import UserServiceDependency, UnitOfWorkDependency
from src.schemas.users import UserResponse

router = APIRouter(prefix="/users", tags=["users"])

@router.get('/', response_model=UserResponse)
async def get_user_by_username(username: str, u_service: UserServiceDependency, uow: UnitOfWorkDependency):
    return await u_service.get_user_by_username(username, uow)

@router.get('/{user_id}', response_model=UserResponse)
async def get_user_by_id(user_id: str, u_service: UserServiceDependency, uow: UnitOfWorkDependency):
    return await u_service.get_user_by_id(uuid.UUID(user_id), uow)


@router.patch('/{user_id}', response_model=UserResponse)
async def update_user(user_id: str, update_data: UserUpdateRequest, current_user: CurrentUserDependency, u_service: UserServiceDependency, uow: UnitOfWorkDependency):
    return await u_service.update_user(update_data=update_data, current_user=current_user, uow=uow, user_id=uuid.UUID(user_id))