from fastapi import Request, Response

from app.utils.jwt import create_token, get_token, set_token, validate_exp_token, validate_payload_fields
from app.repositories.interfaces.abc_base_uow import IBaseUOW
from app.services.exceptions.user import UserServiceException
from app.utils.hashing import check_pwd, get_hash
from app.utils.exceptions import AbsenceAccessJWTExc, AbsenceRefreshJWTExc, TimeExpireAccessJWTExc, TimeExpireRefreshJWTExc
from app.core.config import settings
from app.schemas.dto import UserDTO
from app.repositories.exceptions.base_exc import RepositoryExc

class UserService:
    def __init__(self, uow: IBaseUOW):
        self.uow = uow
        
    async def login(self, response: Response, email: str, pwd: str) -> None:
        try:
            user_by_email = (await self.uow.user_repo.get_by_filters(email=email))
        except RepositoryExc as e:
            raise UserServiceException("User repository: failed get by email", status_code=500)
        
        if len(user_by_email) == 0:
            raise UserServiceException("Неверный email", status_code=401)
        if not check_pwd(pwd, user_by_email[0].hashed_password):
            raise UserServiceException("Неверный пароль", status_code=401)
        access_token = create_token(email=email, type="access")
        refresh_token = create_token(email=email, type="refresh")
        set_token(response, access_token, "access")
        set_token(response, refresh_token, "refresh")
        
    async def authentication(self, request: Request, response: Response) -> UserDTO:
        """Аутентификация пользователя с автоматическим обновлением токенов"""
        
        # Сначала пробуем access token
        try:
            token = get_token(
                type_="access",
                name_token=settings.JWT_ACCESS_TOKEN_NAME,
                request=request
            )
            validate_payload_fields(token)
            validate_exp_token(type_="access", payload=token)
            email = token["user_email"]
            
        except (AbsenceAccessJWTExc, TimeExpireAccessJWTExc):
            try:
            # Если access недоступен/истёк - пробуем refresh
                token = get_token(
                    type_="refresh",
                    name_token=settings.JWT_REFRESH_TOKEN_NAME,
                    request=request
                )
            
                validate_payload_fields(token)
                validate_exp_token(type_="refresh", payload=token)
            except (AbsenceRefreshJWTExc, TimeExpireRefreshJWTExc) as e:
                raise UserServiceException(
                    "Необходима повторная авторизация",
                    status_code=401
                ) from e
            email = token["user_email"]
            
            # Обновляем access token
            access_token = create_token(email=email, type="access")
            set_token(response, access_token, "access")
        except ValueError as e:
           raise UserServiceException(
                "Ошибка валидации токена",
                status_code=422
            ) from e
        
        # Получаем пользователя (один раз для обоих сценариев)
        try:
            users = await self.uow.user_repo.get_by_filters(email=email)
        except RepositoryExc:
            raise UserServiceException(
                "Ошибка при получении данных пользователя",
                status_code=500
            )
        
        if not users:
            raise UserServiceException(
                "Пользователь не найден. Пройдите регистрацию",
                status_code=401
            )
        
        return users[0]
            
    async def register(self, email: str, pwd: str) -> None:
        try:
            user_by_email = (await self.uow.user_repo.get_by_filters(email=email))
        except RepositoryExc as e:
            raise UserServiceException("User repository: failed get by email", status_code=500)
        
        if len(user_by_email) != 0:
            raise UserServiceException("Пользователь с таким email уже существует", status_code=409)
        
        try:
            id = (await self.uow.user_repo.add({"email": email, "hashed_password": get_hash(pwd)}))
            return id
        except RepositoryExc as e:
            raise UserServiceException("User repository: failed add user", status_code=500)
        