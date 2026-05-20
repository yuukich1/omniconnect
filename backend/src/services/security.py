from datetime import datetime, timedelta
import hashlib
import jwt
from src.core.config import settings

class SecurityService:
    
    def hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password: str, hashed: str) -> bool:
        return self.hash_password(password) == hashed
    
    def _generate_token(self, payload: dict, secret_key: str) -> str:
        return jwt.encode(payload, secret_key, algorithm="HS256")

    def create_access_token(self, user_id: int) -> str:
        payload = {
            "user_id": user_id,
            "exp": datetime.utcnow() + timedelta(seconds=settings.EXPIRE_IN)
        }
        return self._generate_token(payload, settings.SECRET_KEY)
    
    def create_refresh_token(self, user_id: int) -> str:
        payload = {
            "user_id": user_id,
            "exp": datetime.utcnow() + timedelta(seconds=settings.EXPIRE_REFRESH_TOKEN_IN)
        }
        return self._generate_token(payload, settings.SECRET_REFRESH_KEY)
    
    
    def decode_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            raise Exception("Token has expired")
        except jwt.InvalidTokenError:
            raise Exception("Invalid token")
        
    