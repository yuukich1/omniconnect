from typing import Annotated
from fastapi import Depends
from src.services.connect_manager import ConnectionManager
from src.services.uow import UnitOfWork
from src.core.connection import async_session_maker


_uow = UnitOfWork(async_session_maker)
_conn_manager = ConnectionManager()

ConnectManagerDepedency = Annotated[ConnectionManager, Depends(lambda: _conn_manager)]
UnitOfWorkDependency = Annotated[UnitOfWork, Depends(lambda: _uow)]