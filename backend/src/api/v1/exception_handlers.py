from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
import src.core.exceptions as exc

def register_exception_handlers(app: FastAPI) -> None:
    

    @app.exception_handler(exc.UserAlreadyExistsError)
    async def user_already_exists_handler(request: Request, e: exc.UserAlreadyExistsError):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": str(e)}, 
        )