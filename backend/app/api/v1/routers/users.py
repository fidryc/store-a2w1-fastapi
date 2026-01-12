from fastapi import HTTPException, Response, APIRouter
from app.api.v1.dependency.uow import UOWDep

from app.api.v1.dependency.user import CurrentUserDep
from app.services.exceptions.user import UserServiceException
from app.services.implementations.user_service import UserService
from app.core.logger import logger
from app.utils.jwt.jwt import set_token

router = APIRouter(
    prefix="/api/v1/users",
    tags=["Регистрация и вход в аккаунт"]
)

@router.get("/login")
async def login(response: Response, email: str, pwd: str, uow: UOWDep):
    try:
        user_service = UserService(uow)
        new_tokens = await user_service.login(email=email, pwd=pwd)
        set_token(response, new_tokens.access_token, "access")
        set_token(response, new_tokens.refresh_token, "refresh")
    except UserServiceException as e:
        raise HTTPException(status_code=e.status_code, detail=e.args[0])
    except Exception as e:
        logger.critical("Unknow error in login", exc_info=True, extra={"email": email, "pwd": pwd})
        raise HTTPException(status_code=500, detail=e.args[0])