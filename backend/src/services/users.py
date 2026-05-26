

from src.services.uow import IUnitOfWork
from src.core.exceptions.auth import UserNotFoundError

class UserService:
    
    async def get_by_username(self, username: str, uow: IUnitOfWork):
        async with uow:
            user = await uow.users.get_by_username(username)
            if not user:
                raise UserNotFoundError()
            return user