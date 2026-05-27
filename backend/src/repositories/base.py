from abc import ABC, abstractmethod
from typing import Generic, List, Optional, TypeVar
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from functools import wraps
from src.api.exceptions import exceptions as exc
class IRepository(ABC):
    
    @abstractmethod
    async def create(self, obj): ... 
    
    @abstractmethod
    async def get(self, id): ...
    
    @abstractmethod
    async def list(self, **filters): ...
    
    @abstractmethod
    async def update(self, id, obj): ...
    
    @abstractmethod
    async def delete(self, id): ...
    
T = TypeVar('T')
    
def handle_db_errors(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except IntegrityError as e:
            error_msg = str(e.orig).upper()
            if "23505" in error_msg or "UNIQUE" in error_msg:
                raise exc.AlreadyExistsError
            if "23503" in error_msg or "FOREIGN KEY" in error_msg:
                raise exc.ForeignKeyError
            if "23514" in error_msg or "CHECK" in error_msg:
                raise exc.DataIntegrityError
            raise e
    return wrapper    
    
class SqlAclehmyRepository(IRepository, Generic[T]):
    
    model: type[T]
    
    def __init__(self, session: AsyncSession):
        self.session = session
        
        
    @handle_db_errors
    async def create(self, obj) -> T:
        self.session.add(obj)
        await self.session.flush()
        return obj
    
    
    @handle_db_errors
    async def get(self, id) -> Optional[T]:
        return await self.session.get(self.model, id)
    
    
    @handle_db_errors
    async def list(self, **filters) -> List[T]:
        query = select(self.model)
        for attr, value in filters.items():
            query = query.filter(getattr(self.model, attr) == value)
        result = await self.session.execute(query)
        return list(result.scalars().all())
    
    
    @handle_db_errors
    async def update(self, id, obj) -> Optional[T]:
        existing = await self.get(id)
        if not existing:
            return None
        for attr, value in obj.items():
            if hasattr(existing, attr):
                setattr(existing, attr, value)
        await self.session.flush()
        return existing
    
    
    @handle_db_errors
    async def delete(self, id) -> bool:
        existing = await self.get(id)
        if not existing:
            return False
        await self.session.delete(existing)
        await self.session.flush()
        return True