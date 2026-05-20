from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
import src.core.exceptions.auth as user_exc
from src.core.exceptions.bots import BotPermissionError, BotNotFoundError, ChatNotFoundError

def register_exception_handlers(app: FastAPI) -> None:
    
    @app.exception_handler(user_exc.UserAlreadyExistsError)
    async def user_already_exists_handler(request: Request, e: user_exc.UserAlreadyExistsError):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": str(e)}, 
        )

    @app.exception_handler(user_exc.UserCredentialError)
    async def user_credential_handler(request: Request, e: user_exc.UserCredentialError):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": str(e)},
        )

    @app.exception_handler(user_exc.UserNotFoundError)
    async def user_not_found_handler(request: Request, e: user_exc.UserNotFoundError):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": str(e)},
        )

    @app.exception_handler(user_exc.TokenPayloadError)
    async def token_payload_handler(request: Request, e: user_exc.TokenPayloadError):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": str(e)},
        )
        
    @app.exception_handler(BotNotFoundError)
    async def bot_not_found_handler(request: Request, e: BotNotFoundError):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": str(e)},
        )
        
    @app.exception_handler(ChatNotFoundError)
    async def chat_not_found_handler(request: Request, e: ChatNotFoundError):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": str(e)},
        )
        
    @app.exception_handler(BotPermissionError)
    async def bot_permission_handler(request: Request, e: BotPermissionError):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": str(e)},
        )