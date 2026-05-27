from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from src.core.config import settings

async_engine = create_async_engine(settings.database_url_async, echo=True)

async_session_maker = async_sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)