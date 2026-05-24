from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
import src.core.exceptions.auth as user_exc
import src.core.exceptions.bots as bot_exc
import src.core.exceptions.chats as chat_exc


EXCEPTION_MAP = {
    user_exc.UserAlreadyExistsError: status.HTTP_409_CONFLICT,
    user_exc.UserCredentialError: status.HTTP_401_UNAUTHORIZED,
    user_exc.CredentialTokenError: status.HTTP_401_UNAUTHORIZED,
    user_exc.TokenPayloadError: status.HTTP_401_UNAUTHORIZED,
    user_exc.TokenExpiredError: status.HTTP_401_UNAUTHORIZED,
    user_exc.TokenInvalidError: status.HTTP_401_UNAUTHORIZED,
    user_exc.UserNotFoundError: status.HTTP_404_NOT_FOUND,
    
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