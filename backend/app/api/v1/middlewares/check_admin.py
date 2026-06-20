from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse

from app.repositories.implementations.sqlalchemy.base_uow import BaseUOW
from app.services.implementations.user_service import UserService
from app.services.exceptions.user import UserServiceException
from app.schemas.dataclasses import AuthTokens
from app.core.config import settings
from app.utils.jwt_utils.jwt_utils import set_token


class IsAdminMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        async with BaseUOW() as uow:
            user_service = UserService(uow)
            auth_tokens = AuthTokens(
                access_token=request.cookies.get(settings.JWT_ACCESS_TOKEN_NAME),
                refresh_token=request.cookies.get(settings.JWT_REFRESH_TOKEN_NAME),
                is_access_token_update=False,
                is_refresh_token_update=False
            )

            try:
                new_auth_tokens = await user_service.refresh_tokens(auth_tokens)
                user = await user_service.get_user_from_token(new_auth_tokens)

                if user.role != "admin":
                    return JSONResponse(
                        status_code=403,
                        content={"detail": "Нет прав для входа в админ-панель"}
                    )

            except UserServiceException:
                return JSONResponse(
                    status_code=401,
                    content={"detail": "Требуется авторизация"},
                )
        
        response = await call_next(request)

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

        return response