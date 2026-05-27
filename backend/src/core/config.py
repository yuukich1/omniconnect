from pydantic_settings import BaseSettings 

class Settings(BaseSettings):
    database_url_sync: str = 'postgresql://username:password@localhost/dbname'
    database_url_async: str = 'postgresql+asyncpg://username:password@localhost/dbname'
    encryption_key: str = 'your-32-byte-base64-encoded-key-here'  # Must be 32 url-safe base64-encoded bytes
    expire_in: int = 3600  # 1 hour
    expire_refresh_token_in: int = 86400  # 24 hours
    secret_key: str = 'your-secret-key-for-jwt'
    secret_refresh_key: str = 'your-secret-refresh-key-for-jwt'
    
    model_config = {
        'env_file': '.env',
        'env_file_encoding': 'utf-8',
    }
    
settings = Settings()