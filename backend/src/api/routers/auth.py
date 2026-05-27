from fastapi import APIRouter, Request
from src.api.dependencies.service import AuthServiceDependency, SecurityServiceDependency, UnitOfWorkDependency
from src.schemas import CreateBaseResponse, StatusReponse
from src.schemas.auth import AuthRequest, TokenReponse
from fastapi.responses import JSONResponse
from src.api.exceptions import exceptions as exc

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post('/register', response_model=CreateBaseResponse, status_code=201)
async def register_user(
    user_data: AuthRequest,
    a_service: AuthServiceDependency,
    s_service: SecurityServiceDependency,
    uow: UnitOfWorkDependency
):
    user = await a_service.create_user(user_data, s_service, uow)
    return CreateBaseResponse(id=user.id)


@router.post('/login', response_model=TokenReponse)
async def login_user(
    user: AuthRequest,
    request: Request,
    a_service: AuthServiceDependency,
    s_service: SecurityServiceDependency,
    uow: UnitOfWorkDependency
):
    ip = request.client.host # type: ignore
    user_agent = request.headers.get('User-Agent', 'unknown')
    token_data = await a_service.login_user(user.username, user.password, user_agent, ip, s_service, uow)
    response = JSONResponse(content=TokenReponse(
        access_token=token_data.access_token,
        token_type='bearer',
        expires_in=token_data.access_token_expires_in
    ).model_dump())
    response.set_cookie(
        key='refresh_token',
        value=token_data.refresh_token,
        httponly=True,
        # secure=True,
        samesite='lax',
        max_age=token_data.refresh_token_expires_in
    )
    return response

@router.post('/refresh', response_model=TokenReponse)
async def refresh_token(
    request: Request,
    a_service: AuthServiceDependency,
    s_service: SecurityServiceDependency,
    uow: UnitOfWorkDependency
):
    refresh_token = request.cookies.get('refresh_token')
    if not refresh_token:
        raise exc.AuthenticationError
    ip = request.client.host # type: ignore
    user_agent = request.headers.get('User-Agent', 'unknown')
    new_token_data = await a_service.refresh_token(refresh_token, user_agent, ip, s_service, uow)
    response = JSONResponse(content=TokenReponse(
        access_token=new_token_data.access_token,
        token_type='bearer',
        expires_in=new_token_data.access_token_expires_in
    ).model_dump())
    response.set_cookie(
        key='refresh_token',
        value=new_token_data.refresh_token,
        httponly=True,
        # secure=True,
        samesite='lax',
        max_age=new_token_data.refresh_token_expires_in
    )
    return response

@router.post('/logout', response_model=StatusReponse)
async def logout_user(
    request: Request,
    a_service: AuthServiceDependency,
    s_service: SecurityServiceDependency,
    uow: UnitOfWorkDependency
):
    refresh_token = request.cookies.get('refresh_token')
    if not refresh_token:
        raise exc.AuthenticationError
    await a_service.revoke_token(refresh_token, s_service, uow)
    response = JSONResponse(content=StatusReponse(status='ok').model_dump())
    response.delete_cookie('refresh_token')
    return response
    
    