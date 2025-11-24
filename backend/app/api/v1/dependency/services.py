from typing import Annotated
from fastapi import Depends
from app.services.implementations.user_service import UserService
from app.api.v1.dependency.uow import UOWDep


def get_user_service(uow: UOWDep) -> UserService:
    return UserService(uow)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]