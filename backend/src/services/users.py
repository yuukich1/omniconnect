from typing import Optional
import uuid

from src.schemas.auth import CurrentUser
from src.services.uow import IUnitOfWork
from src.api.exceptions import exceptions as exc
from src.schemas.users import UserChangePasswordRequest, UserResponse, UserUpdateRequest

class UserService:
    
    async def get_user_by_id(self, user_id: uuid.UUID, uow: IUnitOfWork) -> UserResponse:
        async with uow:
            user = await uow.users.get(user_id)
            if not user:
                raise exc.NotFoundError("User not found")
            return UserResponse(
                id=user.id,
                username=user.username,
                role=user.role
            )
            
    async def get_list_user(self, uow: IUnitOfWork):
        async with uow:
            users = await uow.users.list()
            return [UserResponse(id=user.id, username = user.username, role=user.role) for user in users]
            
    async def get_user_by_username(self, username: str, uow: IUnitOfWork) -> UserResponse:
        async with uow:
            user = await uow.users.get_by_username(username)
            if not user:
                raise exc.NotFoundError("User not found")
            return UserResponse(
                id=user.id,
                username=user.username,
                role=user.role
            )
            
    async def update_user(self, update_data: UserUpdateRequest,  current_user: CurrentUser, uow: IUnitOfWork, user_id: Optional[uuid.UUID] = None) -> UserResponse:
        async with uow:
            if user_id is None:
                user_id = current_user.id
            elif current_user.role != 'admin' and user_id != current_user.id:
                raise exc.AuthorizationError("You don't have permission to update this user")
            user = await uow.users.get(user_id)
            if not user:
                raise exc.NotFoundError("User not found")
            if update_data.username is not None:
                user.username = update_data.username
            if update_data.role is not None:
                if current_user.role != 'admin':
                    raise exc.AuthorizationError("Only admin can update user role")
                user.role = update_data.role
            await uow.commit()
            return UserResponse(
                id=user.id,
                username=user.username,
                role=user.role
            )
            
    async def change_password(self, change_data: UserChangePasswordRequest, current_user: CurrentUser, uow: IUnitOfWork) -> None:
        async with uow:
            user = await uow.users.get(current_user.id)
            if not user:
                raise exc.NotFoundError("User not found")
            if not user.verify_password(change_data.old_password):
                raise exc.AuthorizationError("Old password is incorrect")
            hashed_password = user.hash_password(change_data.new_password)
            user.password = hashed_password
            await uow.commit()
            return 
        
    async def delete_user(self, user_id: uuid.UUID, uow: IUnitOfWork) -> None:
        async with uow:
            user = await uow.users.get(user_id)
            if not user:
                raise exc.NotFoundError("User not found")
            await uow.users.delete(user_id)
            await uow.commit()
            return