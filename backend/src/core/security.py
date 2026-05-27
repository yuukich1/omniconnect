from cryptography.fernet import Fernet
from fastapi.security import OAuth2PasswordBearer
from .config import settings

fernet = Fernet(settings.encryption_key)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v0.2/auth/token", refreshUrl="api/v0.2/auth/refresh")