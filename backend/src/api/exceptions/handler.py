from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
import jwt

from src.api.exceptions import exceptions as exc


EXCEPTION_MAP = {
    exc.AlreadyExistsError: status.HTTP_409_CONFLICT,
    exc.ForeignKeyError: status.HTTP_400_BAD_REQUEST,
    exc.DataIntegrityError: status.HTTP_422_UNPROCESSABLE_ENTITY,
    exc.AuthenticationError: status.HTTP_401_UNAUTHORIZED,
    exc.AuthorizationError: status.HTTP_403_FORBIDDEN,
    jwt.InvalidTokenError: status.HTTP_401_UNAUTHORIZED,
    jwt.ExpiredSignatureError: status.HTTP_401_UNAUTHORIZED,
    exc.NotFoundError: status.HTTP_404_NOT_FOUND,
}

def register_exception_handlers(app: FastAPI) -> None:
    for exc_class, status_code in EXCEPTION_MAP.items():
        async def generic_handler(request: Request, exc: Exception):
            return JSONResponse(
                status_code=status_code, 
                content={"detail": str(exc)},
            )
        app.add_exception_handler(exc_class, generic_handler)