from fastapi import HTTPException, Response, APIRouter
from app.api.v1.dependency.uow import UOWDep
from app.repositories.implementations.sqlalchemy.base_uow import BaseUOW
import aiofiles

from app.api.v1.dependency.user import AdminDep
from app.services.exceptions.user import UserServiceException
from app.services.implementations.user_service import UserService
from app.core.logger import logger

router = APIRouter(
    prefix="/api/v1/users",
    tags=["Регистрация и вход в аккаунт"]
)

@router.get("/login")
async def test(response: Response, email: str, pwd: str, uow: UOWDep):
    try:
        user_service = UserService(uow)
        await user_service.login(response, email=email, pwd=pwd)
    except UserServiceException as e:
        raise HTTPException(status_code=e.status_code, detail=e.args[0])
    except Exception as e:
        logger.critical("Unknow error in login", exc_info=True, extra={"email": email, "pwd": pwd})
        raise HTTPException(status_code=e.status_code, detail=e.args[0])