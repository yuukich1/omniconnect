from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
import src.core.exceptions.auth as auth_exc
import src.core.exceptions.bots as bot_exc
import src.core.exceptions.chats as chat_exc


EXCEPTION_MAP = {
    auth_exc.UserAlreadyExistsError: status.HTTP_409_CONFLICT,
    auth_exc.UserCredentialError: status.HTTP_401_UNAUTHORIZED,
    auth_exc.CredentialTokenError: status.HTTP_401_UNAUTHORIZED,
    auth_exc.TokenPayloadError: status.HTTP_401_UNAUTHORIZED,
    auth_exc.TokenExpiredError: status.HTTP_401_UNAUTHORIZED,
    auth_exc.TokenInvalidError: status.HTTP_401_UNAUTHORIZED,
    auth_exc.UserNotFoundError: status.HTTP_404_NOT_FOUND,
    auth_exc.CoflitUserError: status.HTTP_409_CONFLICT,
    
    bot_exc.BotNotFoundError: status.HTTP_404_NOT_FOUND,
    bot_exc.BotPermissionError: status.HTTP_403_FORBIDDEN,
    bot_exc.WebhookCreateMessageError: status.HTTP_400_BAD_REQUEST,
    bot_exc.MediaGroupSendError: status.HTTP_400_BAD_REQUEST,
    
    chat_exc.ChatNotFoundError: status.HTTP_404_NOT_FOUND,
}

def register_exception_handlers(app: FastAPI) -> None:
    for exc_class, status_code in EXCEPTION_MAP.items():
        async def generic_handler(request: Request, exc: Exception, code=status_code):
            return JSONResponse(
                status_code=code,
                content={"detail": str(exc)},
            )
        
        app.add_exception_handler(exc_class, generic_handler)