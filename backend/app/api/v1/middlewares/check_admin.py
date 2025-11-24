from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import HTTPException, Request, Response
from fastapi.responses import JSONResponse

from app.repositories.implementations.sqlalchemy.base_uow import BaseUOW
from app.services.implementations.user_service import UserService


class IsAdminMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        # Проверяем роль пользователя
        async with BaseUOW() as uow:
            user_service = UserService(uow)
            user = await user_service.authentication(request=request, response=response)
            if user and user.role == "admin":
                return response

            return JSONResponse(
                status_code=403,
                content={"detail": "У вас нет прав для входа в админ-панель"}
            )