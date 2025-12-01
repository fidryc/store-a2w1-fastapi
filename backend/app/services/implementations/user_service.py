from app.core.logger import logger

from app.utils.jwt import create_token, get_token_payload, validate_payload_fields
from app.repositories.interfaces.abc_base_uow import IBaseUOW
from app.services.exceptions.user import UserServiceException
from app.utils.hashing import check_pwd, get_hash
from app.utils.exceptions import AbsenceAccessJWTExc, AbsenceRefreshJWTExc, TimeExpireAccessJWTExc, TimeExpireRefreshJWTExc
from app.schemas.dto import UserDTO
from app.repositories.exceptions.base_exc import RepositoryExc
from app.schemas.dataclasses import AuthTokens
from app.services.interfaces.abc_user_service import IUserService

class UserService(IUserService):
    def __init__(self, uow: IBaseUOW):
        self.uow = uow
        
    async def login(self, email: str, pwd: str) -> AuthTokens:
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
        auth_tokens = AuthTokens(access_token, refresh_token, True, True)
        return auth_tokens
        
    async def refresh_tokens(self, auth_tokens: AuthTokens) -> AuthTokens:
        """Проверка и получение новых токенов для аутенфикации. Refresh токен пока не обновляется для безопасности"""
        
        # Сначала пробуем access token
        try:
            if not auth_tokens.access_token:
                raise AbsenceAccessJWTExc
            
            token_payload = get_token_payload(
                type_="access",
                token=auth_tokens.access_token
            )
            validate_payload_fields(type_="access", token_payload=token_payload)
            email = token_payload["user_email"]
        except (AbsenceAccessJWTExc, TimeExpireAccessJWTExc):
            # Если access недоступен/истёк - пробуем refresh
            try:
                if not auth_tokens.refresh_token:
                    raise AbsenceRefreshJWTExc
                
                token_payload = get_token_payload(
                    type_="refresh",
                    token=auth_tokens.refresh_token
                )
                validate_payload_fields(type_="refresh", token_payload=token_payload)
            except (AbsenceRefreshJWTExc, TimeExpireRefreshJWTExc) as e:
                raise UserServiceException(
                    "Необходима повторная авторизация",
                    status_code=401
                ) from e
            email = token_payload["user_email"]
            
            # Обновляем access token
            new_access_token = create_token(email=email, type="access")
            auth_tokens.access_token = new_access_token
            auth_tokens.is_access_token_update = True
        except ValueError as e:
           raise UserServiceException(
                "Ошибка валидации токена",
                status_code=422
            ) from e
           
        return auth_tokens
           
    async def get_user_from_token(self, auth_tokens: AuthTokens) -> UserDTO:
        """Получение user из токенов"""
        access_token_payload = get_token_payload(type_="access", token=auth_tokens.access_token)
        try:
            user = await self.uow.user_repo.get_by_filters(email=access_token_payload["user_email"])
        except RepositoryExc as e:
            logger.critical("User repository error: Failed get user by email")
            raise UserServiceException("Failed get user by email", status_code=500) from e
        
        if not user:
            raise UserServiceException("Not found user. You should register", status_code=401)
        return user[0]
    
            
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
        