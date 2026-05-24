from fastapi.security import OAuth2PasswordBearer
from pydantic_settings import BaseSettings
from cryptography.fernet import Fernet
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from aiogram.client.session.aiohttp import AiohttpSession

class Settings(BaseSettings):
    ENCRYPTION_KEY: str = 'KEY'
    DATABASE_URL: str = 'database_url'
    SECRET_KEY: str = 'secret_key'
    SECRET_REFRESH_KEY: str = 'secret_refresh_key'
    EXPIRE_IN: int = 3600
    EXPIRE_REFRESH_TOKEN_IN: int = 86400
    UPLOAD_DIR: str = "uploads"
    
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore"
    }

settings = Settings()

fernet = Fernet(settings.ENCRYPTION_KEY)

async_engine = create_async_engine(settings.DATABASE_URL)

async_session_maker = async_sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/token", refreshUrl="api/v1/auth/refresh")

session_tg_bot = AiohttpSession()