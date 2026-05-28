from datetime import datetime, timedelta, timezone

from src.schemas.auth import AuthRequest

from .uow import IUnitOfWork
from .security import SecurityService
from src.models import User, RefreshToken
from src.api.exceptions import exceptions as exc

class AuthService:
    
    async def create_user(self, user_data: AuthRequest, s_service: SecurityService, uow: IUnitOfWork):
        hashed_password = s_service.hash_password(user_data.password)
        user_model = User(username=user_data.username, hashed_password=hashed_password)
        async with uow:
            user = await uow.users.create(user_model)
            await uow.commit()
            return user

    async def login_user(self, username: str, password: str, user_agent: str, ip: str, s_service: SecurityService, uow: IUnitOfWork):
        async with uow:
            user = await uow.users.get_by_username(username)
            if not user or not s_service.verify_password(password, user.hashed_password):
                raise exc.AuthenticationError
            token_data = s_service.generate_pair(user.id, user.username, 'user')
            expires_at = datetime.now(timezone.utc) + timedelta(seconds=token_data.refresh_token_expires_in)
            await uow.refresh_token.create(RefreshToken(
                jti=token_data.jwi,
                user_id=user.id,
                expires_at=expires_at,
                user_agent=user_agent,
                ip_address=ip,
            ))
            await uow.commit()
            return token_data
        
    async def refresh_token(self, refresh_token: str, user_agent: str, ip: str, s_service: SecurityService, uow: IUnitOfWork):
        payload = s_service.verify_token(refresh_token, token_type='refresh')
        jti = payload.get('jti')
        if not jti:
            raise exc.AuthenticationError
        async with uow:
            token_record = await uow.refresh_token.get_by_jti(jti)
            if not token_record or token_record.is_revoked or token_record.expires_at < datetime.now(timezone.utc):
                raise exc.AuthenticationError
            user = await uow.users.get(token_record.user_id)
            if not user:
                raise exc.AuthenticationError
            new_token_data = s_service.generate_pair(user.id, user.username, 'user')
            token_record.is_revoked = True
            expires_at = datetime.now(timezone.utc) + timedelta(seconds=new_token_data.refresh_token_expires_in)
            await uow.refresh_token.create(RefreshToken(
                jti=new_token_data.jwi,
                user_id=user.id,
                expires_at=expires_at,
                user_agent=user_agent,
                ip_address=ip,
            ))
            await uow.commit()
            return new_token_data
        
    async def revoke_token(self, refresh_token: str, s_service: SecurityService, uow: IUnitOfWork):
        payload = s_service.verify_token(refresh_token, token_type='refresh')
        jti = payload.get('jti')
        if not jti:
            raise exc.AuthenticationError
        async with uow:
            token_record = await uow.refresh_token.get_by_jti(jti)
            if token_record:
                token_record.is_revoked = True
                await uow.commit()
                return 
        