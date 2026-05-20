from src.core.config import async_session_maker
from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
import src.repositories as repo


class IUnitOfWork(ABC):
    
    bots: repo.BotsRepository
    chats: repo.ChatRepository
    message: repo.MessageRepository
    token: repo.RefreshTokenRepository
    users: repo.UserRepository
    
    @abstractmethod
    async def __aenter__(self): ...

        
    @abstractmethod
    async def __aexit__(self, exc_type, exc, tb): ...
        
        
    @abstractmethod
    async def commit(self): ...
    
    @abstractmethod
    async def rollback(self): ...
    
    
class UnitOfWork(IUnitOfWork):
    
    def __init__(self):
        self.session_factory = async_session_maker
        
    async def __aenter__(self):
        self.session: AsyncSession = self.session_factory()
        
        self.bots = repo.BotsRepository(self.session)
        self.chats = repo.ChatRepository(self.session)
        self.message = repo.MessageRepository(self.session)
        self.token = repo.RefreshTokenRepository(self.session)
        self.users = repo.UserRepository(self.session)
        
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type:
            await self.rollback()
        else:
            await self.commit()
            
        await self.session.close()
        
    async def commit(self) -> None:
        await self.session.commit()
    
    async def rollback(self) -> None:
        await self.session.rollback()