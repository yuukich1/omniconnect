from datetime import datetime, timedelta
import hashlib
import uuid
import jwt
from src.core.config import settings
from src.schemas.tokens import TokenDTO


class SecurityService:
    
    def hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password: str, hashed: str) -> bool:
        return self.hash_password(password) == hashed
    
    def generate_pair(self, user_id: uuid.UUID, username: str, role: str):
        now = datetime.utcnow()
        jti = str(uuid.uuid4())
        acc_exp = now + timedelta(seconds=settings.expire_in)
        ref_exp = now + timedelta(seconds=settings.expire_refresh_token_in)
        
        access_payload = {
            'sub': str(user_id),
            'username': username,
            'role': role,
            'type': 'access',
            'exp': acc_exp
        }
        refresh_payload = {
            'sub': str(user_id),
            'username': username,
            'role': role,
            'jti': jti,
            'type': 'refresh',
            'exp': ref_exp
        }
        access_token = jwt.encode(access_payload, settings.secret_key, algorithm='HS256')
        refresh_token = jwt.encode(refresh_payload, settings.secret_refresh_key, algorithm='HS256')
        return TokenDTO(
            access_token=access_token,
            refresh_token=refresh_token,
            jwi=jti,
            access_token_expires_in=settings.expire_in,
            refresh_token_expires_in=settings.expire_refresh_token_in
        )
    
    def verify_token(self, token: str, token_type: str = 'access'):
        secret = settings.secret_key if token_type == 'access' else settings.secret_refresh_key
        try:
            payload = jwt.decode(token, secret, algorithms=['HS256'])
            if payload.get('type') != token_type:
                raise jwt.InvalidTokenError
            return payload
        except jwt.ExpiredSignatureError:
            raise 
        except jwt.InvalidTokenError:
            raise 
        
    
        
        