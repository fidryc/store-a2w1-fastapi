from typing import Annotated
from fastapi import Depends, HTTPException, Response, Request
from app.api.v1.dependency.services import UserServiceDep
from app.schemas.dto import UserDTO
from app.services.exceptions.user import UserServiceException
from app.schemas.dataclasses import AuthTokens
from app.core.config import settings
from app.utils.jwt_utils.jwt_utils import set_token
    
    
async def get_auth_tokens(request: Request) -> AuthTokens:
    return AuthTokens(
        access_token=request.cookies.get(settings.JWT_ACCESS_TOKEN_NAME, None),
        refresh_token=request.cookies.get(settings.JWT_REFRESH_TOKEN_NAME, None),
        is_access_token_update=False,
        is_refresh_token_update=False
    )
    
    
async def get_user(
    response: Response,
    user_service: UserServiceDep,
    auth_tokens = Depends(get_auth_tokens)
):
    try:
        new_auth_tokens = await user_service.refresh_tokens(auth_tokens=auth_tokens)
        if new_auth_tokens.is_access_token_update:
            set_token(
                response=response,
                token=new_auth_tokens.access_token,
                type_="access"
            )
        if new_auth_tokens.is_refresh_token_update:
            set_token(
                response=response,
                token=new_auth_tokens.refresh_token,
                type_="refresh"
            )
            new_auth_tokens.is_refresh_token_update = False
        user = await user_service.get_user_from_token(auth_tokens=new_auth_tokens)
        return user
    except UserServiceException as e:
        raise HTTPException(
            e.status_code,
            "Пользователь не зарегестрирован",
            )

CurrentUserDep = Annotated[UserDTO, Depends(get_user)]


async def get_admin(user: CurrentUserDep):
    if user.role != "admin":
        raise HTTPException(
            status_code=403, 
            detail="Требуются права администратора"
        )
    return user


AdminDep = Annotated[UserDTO, Depends(get_admin)]