from typing import Annotated
from fastapi import Depends

from src.services.users import UsersService
from src.services.uow import IUnitOfWork, UnitOfWork

async def get_uow() -> IUnitOfWork:
    return UnitOfWork()

UowDep = Annotated[IUnitOfWork, Depends(get_uow)]


_users_service = UsersService()


def get_users_service() -> UsersService:
    return _users_service


UsersServiceDep = Annotated[UsersService, Depends(get_users_service)]
