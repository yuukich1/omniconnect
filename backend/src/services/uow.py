from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
import src.repositories as repo


class IUnitOfWork(ABC):
    
    users: repo.UserRepository
    refresh_token: repo.RefreshTokenRepository
    chat: repo.ChatsRepository
    chat_members: repo.ChatMembersRepository
    message: repo.MessageRepository
    
    
    @abstractmethod
    async def __aenter__(self): ...

        
    @abstractmethod
    async def __aexit__(self, exc_type, exc, tb): ...
        
        
    @abstractmethod
    async def commit(self): ...
    
    @abstractmethod
    async def rollback(self): ...
    
    
class UnitOfWork(IUnitOfWork):
    
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session: AsyncSession = self.session_factory()
        self.users = repo.UserRepository(self.session)
        self.refresh_token = repo.RefreshTokenRepository(self.session)
        self.chat = repo.ChatsRepository(self.session)
        self.chat_members = repo.ChatMembersRepository(self.session)
        self.message = repo.MessageRepository(self.session)

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