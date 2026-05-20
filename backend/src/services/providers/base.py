from abc import ABC, abstractmethod

class IPlatformBotsService(ABC):
    
    @abstractmethod
    async def save_message(self): ...