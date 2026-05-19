from pydantic_settings import BaseSettings
from cryptography.fernet import Fernet
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

class Settings(BaseSettings):
    ENCRYPTION_KEY: str = 'KEY'
    DATABASE_URL: str = 'database_url'
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore"
    }

settings = Settings()

fernet = Fernet(settings.ENCRYPTION_KEY)

async_engine = create_async_engine(settings.DATABASE_URL)

async_session_maker = async_sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)