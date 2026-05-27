from fastapi import APIRouter
from src.schemas import StatusReponse
from src.schemas.users import UserResponse, UserUpdateRequest, UserChangePasswordRequest
from src.api.dependencies.auth import CurrentUserDependency
from src.api.dependencies.service import UserServiceDependency, UnitOfWorkDependency


router = APIRouter(prefix="/me", tags=["me"])

@router.get('/', response_model=UserResponse)
async def get_current_user(user: CurrentUserDependency, u_service: UserServiceDependency, uow: UnitOfWorkDependency):
    return await u_service.get_user_by_id(user.id, uow)

@router.put('/', response_model=UserResponse)
async def update_current_user(update_data: UserUpdateRequest, user: CurrentUserDependency, u_service: UserServiceDependency, uow: UnitOfWorkDependency):
    return await u_service.update_user(update_data=update_data, current_user=user, uow=uow)

@router.patch('/password', response_model=StatusReponse)
async def change_password(change_data: UserChangePasswordRequest, user: CurrentUserDependency, u_service: UserServiceDependency, uow: UnitOfWorkDependency):
    await u_service.change_password(change_data=change_data, current_user=user, uow=uow)
    return StatusReponse(status='ok')

@router.delete('/', response_model=StatusReponse)
async def delete_current_user(user: CurrentUserDependency, u_service: UserServiceDependency, uow: UnitOfWorkDependency):
    await u_service.delete_user(user_id=user.id, uow=uow)
    return StatusReponse(status='ok')