from loguru import logger
from sqlalchemy.exc import IntegrityError

from src.core.exceptions.auth import UserAlreadyExistsError, UserNotFoundError, UserCredentialError
from src.schemas.users import UserRegister
from .uow import IUnitOfWork
from .security import SecurityService


class AuthService:
    
    
    async def register(self, data: UserRegister, uow: IUnitOfWork):
        user_dict = data.model_dump()
        raw_password = user_dict.pop('password')
        user_dict['hashed_password'] = SecurityService().hash_password(raw_password)
        async with uow: 
            try:
                user = await uow.users.save(user_dict)
                await uow.commit()
                return user
            except IntegrityError as e:
                await uow.rollback()
                error_msg = str(e.orig)
                if "unique" in error_msg.lower() or "already exists" in error_msg.lower():
                    raise UserAlreadyExistsError()
                raise e
                
        
    async def login(self, email: str, password: str, uow: IUnitOfWork):
        async with uow:
            user = await uow.users.get_by_email(email)
            if not user:
                raise UserNotFoundError()
            logger.info(f"User found: {user.email}, hashed_password: {user.hashed_password}")
            if not SecurityService().verify_password(password, user.hashed_password):
                raise UserCredentialError()
            access_token = SecurityService().create_access_token(user.id)
            refresh_token = SecurityService().create_refresh_token(user.id)
            await uow.token.save({"user_id": user.id, "refresh_token": refresh_token})
            await uow.commit()
            return {"access_token": access_token, "refresh_token": refresh_token, "type": "bearer"}
        