from datetime import datetime, timedelta, timezone
from typing import Literal
import uuid

from fastapi import Request, Response
from app.core.config import settings
from jwt import decode, encode
from jwt.exceptions import PyJWTError
from app.core.logger import logger
from app.utils.exceptions import AbsenceAccessJWTExc, AbsenceRefreshJWTExc, TimeExpireAccessJWTExc, TimeExpireJWTExc, TimeExpireRefreshJWTExc


def create_token(email: str, type: str) -> str:
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


def set_token(response: Response, token: str, type):
    """Cохраняет в cookie access или refresh токен в cookie"""
    if type == "access":
        response.set_cookie(settings.JWT_ACCESS_TOKEN_NAME, token, httponly=True)
    if type == "refresh":
        response.set_cookie(
            settings.JWT_REFRESH_TOKEN_NAME,
            token,
            httponly=True,
            max_age=int(timedelta(days=settings.EXP_DAYS_REFRESH_TOKEN).total_seconds()),
        )


def get_token(type_: Literal["access", "refresh"], name_token: str, request: Request) -> dict:
    """Получает payload access токена из cookie"""
    exc = {
        "access": AbsenceAccessJWTExc,
        "refresh": AbsenceRefreshJWTExc
    }
    token = request.cookies.get(name_token, None)
    if not token:
        raise exc[type_]("Нет токена для проверки аккаунт")
    try:
        payload: dict = decode(
            token,
            settings.PUBLIC_SECRET_KEY,
            settings.ALGORITM,
            options={"verify_exp": False},
        )
        if payload.get("type", None) != type_:
            raise ValueError(f"Токен {type_} jwt подделан")
        return payload
    except PyJWTError:
        logger.warning(
            "Failed decode access jwt token", extra={"token": token}, exc_info=True
        )
        raise ValueError("Ошибка декодировки access токена")


def validate_payload_fields(token_payload: dict):
    """Проверка атрибутов payload токена на правильность типов"""
    jti = token_payload.get("jti", None)
    if not jti or not isinstance(jti, str):
        raise ValueError("Неправильное поле jti")
    user_email = token_payload.get("user_email", None)
    if not user_email or not isinstance(user_email, str):
        raise ValueError("Неправильное поле user_email")
    exp = token_payload.get("exp", None)
    if not exp or not isinstance(exp, float):
        raise ValueError("Неправильное поле exp")
    type = token_payload.get("type", None)
    if not type or type not in ("access", "refresh"):
        raise ValueError("Неправильное поле type")


def validate_exp_token(type_: Literal["access", "refresh"], payload: dict) -> None:
    exc = {
        "access": TimeExpireAccessJWTExc,
        "refresh": TimeExpireRefreshJWTExc
    }
    """Выбрасывает исключение TimeExpireJWTExc если вышло время жизни токена"""
    if datetime.now(timezone.utc).timestamp() > payload["exp"]:
        raise exc[type_](f"Время токена истекло {payload["type"]}")
