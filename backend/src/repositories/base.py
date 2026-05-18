from abc import ABC, abstractmethod
from typing import Any, Generic, List, Optional, TypeVar
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

class ABCREpository(ABC):

    def __init__(self, session: AsyncSession):
        self.session = session
    
    @abstractmethod
    async def save(self, data: dict):
        ...

    @abstractmethod
    async def get(self, id: Any):
        ...

    @abstractmethod
    async def get_list(self):
        ...

    @abstractmethod
    async def update(self, id: Any, new_data: dict):
        ...

    @abstractmethod
    async def delete(self, id: Any):
        ... 


T = TypeVar('T')


class SQLAlchemyRepository(ABCREpository, Generic[T]):

    model: type[T] 

    def __init__(self, session: AsyncSession):
        self.session = session
        if not self.model:
            raise NotImplementedError('model cannot be empty')
        
    async def save(self, data: dict) -> T:
        instance = self.model(**data)
        self.session.add(instance)
        await self.session.flush()
        return instance
    
    async def get(self, id: Any) -> Optional[T]:
        return await self.session.get(self.model, id)
    
    async def get_list(self) -> List[T]:
        query = select(self.model)
        result = await self.session.execute(query)
        return list(result.scalars().all())
    
    async def update(self, id: Any, new_data: dict) -> Optional[T]:
        instance = await self.get(id)
        if instance:
            for key, value in new_data.items():
                setattr(instance, key, value)
            await self.session.flush()
        return instance
    
    async def delete(self, id: Any) -> None:
        instance = await self.get(id)
        if instance:
            await self.session.delete(instance)
            await self.session.flush()