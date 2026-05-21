from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
import src.core.exceptions.auth as user_exc
import src.core.exceptions.bots as bot_exc
import src.core.exceptions.chats as chat_exc

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
        
    @app.exception_handler(bot_exc.BotNotFoundError)
    async def bot_not_found_handler(request: Request, e: bot_exc.BotNotFoundError):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": str(e)},
        )
        
    @app.exception_handler(chat_exc.ChatNotFoundError)
    async def chat_not_found_handler(request: Request, e: chat_exc.ChatNotFoundError):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": str(e)},
        )
        
    @app.exception_handler(bot_exc.BotPermissionError)
    async def bot_permission_handler(request: Request, e: bot_exc.BotPermissionError):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": str(e)},
        )
        
    @app.exception_handler(bot_exc.WebhookCreateMessageError)
    async def webhook_create_message_handler(request: Request, e: bot_exc.WebhookCreateMessageError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'detail': str(e)}
        )
        
    @app.exception_handler(user_exc.CredentialTokenError)
    async def credential_token_hadnler(request: Request, e: user_exc.CredentialTokenError):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={'detail': str(e)}
        )