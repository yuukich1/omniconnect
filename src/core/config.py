from pydantic_settings import BaseSettings
from cryptography.fernet import Fernet


class Settings(BaseSettings):
    ENCRYPTION_KEY: str = 'ENCRYPTION_KEY'

settings = Settings()

fernet = Fernet(settings.ENCRYPTION_KEY)