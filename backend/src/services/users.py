import hashlib
from sqlalchemy.exc import IntegrityError
from src.core.exceptions import UserAlreadyExistsError
from src.schemas.users import UserRegister
from .uow import IUnitOfWork

class UsersService:
    
    async def register(self, data: UserRegister, uow: IUnitOfWork):
        user_dict = data.model_dump()
        raw_password = user_dict.pop('password')
        user_dict['hashed_password'] = hashlib.sha256(raw_password.encode()).hexdigest()
        
        async with uow: 
            try:
                user = await uow.users.save(user_dict)
                await uow.commit()
                return user
            except IntegrityError as e:
                await uow.rollback()
                error_msg = str(e.orig)
                if "unique" in error_msg.lower() or "already exists" in error_msg.lower():
                    raise UserAlreadyExistsError("User Already Exists")
                raise e
                
        
        