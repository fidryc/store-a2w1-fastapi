from datetime import datetime, timedelta, timezone
from typing import Literal
import uuid

from fastapi import Response
from app.core.config import settings
from jwt import decode, encode
from jwt.exceptions import PyJWTError
from app.core.logger import logger
from app.utils.jwt_utils.exceptions import TimeExpireAccessJWTExc


def create_token(email: str, type: Literal["access", "refresh"]) -> str:
    """Создает токены access и refresh"""
    jti = str(uuid.uuid4())
    if type == "access":
        time_exp = datetime.now(timezone.utc) + timedelta(seconds=settings.EXP_SEC_ACCESS_TOKEN)
    elif type == "refresh":
        time_exp = datetime.now(timezone.utc) + timedelta(
            days=settings.EXP_DAYS_REFRESH_TOKEN
        )

    payload = {
        "jti": jti,
        "user_email": str(email),
        "exp": time_exp.timestamp(),
        "type": str(type),
    }
    jwt = encode(payload, key=settings.PRIVATE_SECRET_KEY, algorithm=settings.ALGORITM)

    return jwt


def set_token(response: Response, token: str, type_: Literal["access", "refresh"]):
    """Cохраняет в cookie access или refresh токен в cookie"""
    if type_ == "access":
        response.set_cookie(settings.JWT_ACCESS_TOKEN_NAME, token, httponly=True)
    elif type_ == "refresh":
        response.set_cookie(
            settings.JWT_REFRESH_TOKEN_NAME,
            token,
            httponly=True,
            max_age=int(timedelta(days=settings.EXP_DAYS_REFRESH_TOKEN).total_seconds()),
        )


def get_token_payload(token: str) -> dict:
    """Получает payload access токена из cookie"""
    try:
        payload: dict = decode(
            token,
            settings.PUBLIC_SECRET_KEY,
            settings.ALGORITM,
            options={"verify_exp": False},
        )
        return payload
    except PyJWTError:
        logger.warning(
            "Failed decode access jwt token", extra={"token": token}, exc_info=True
        )
        raise ValueError("Ошибка декодировки access токена")


def validate_payload_fields(token_payload: dict, type_: Literal["access", "refresh"]):
    """Полная валидация payload"""
    jti = token_payload.get("jti", None)
    if not jti or not isinstance(jti, str):
        raise ValueError("Неправильное поле jti")
    user_email = token_payload.get("user_email", None)
    if not user_email or not isinstance(user_email, str):
        raise ValueError("Неправильное поле user_email")
    exp = token_payload.get("exp", None)
    if not exp or not isinstance(exp, float):
        raise ValueError("Неправильное поле exp")
    validate_exp_token(type_, exp)
    type = token_payload.get("type", None)
    if not type or type not in ("access", "refresh"):
        raise ValueError("Неправильное поле type")


def validate_exp_token(type_: Literal["access", "refresh"], exp: float) -> None:
    exc = {
        "access": TimeExpireAccessJWTExc,
        "refresh": TimeExpireAccessJWTExc
    }
    """Выбрасывает исключение TimeExpireAccessJWTExc | TimeExpireAccessJWTExc если вышло время жизни токена"""
    if datetime.now(timezone.utc).timestamp() > exp:
        raise exc[type_](f"Время токена истекло {type_}")


def create_delete_cookie_headers():
    """Создает заголовки для удаления куки"""
    # Для удаления куки устанавливаем Max-Age=0 и пустое значение
    access_cookie = f"{settings.JWT_ACCESS_TOKEN_NAME}=; Path=/; Max-Age=0; HttpOnly; SameSite=Lax"
    refresh_cookie = f"{settings.JWT_REFRESH_TOKEN_NAME}=; Path=/; Max-Age=0; HttpOnly; SameSite=Lax"
    
    # Добавьте Secure, если используете HTTPS
    if getattr(settings, 'COOKIE_SECURE', True):
        access_cookie += "; Secure"
        refresh_cookie += "; Secure"
    
    return {
        "Set-Cookie": f"{access_cookie}, {refresh_cookie}"
    }