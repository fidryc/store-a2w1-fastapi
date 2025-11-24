from typing import Annotated
from fastapi import Depends, HTTPException, Response, Request
from app.api.v1.dependency.services import UserServiceDep
from app.schemas.dto import UserDTO
from app.services.exceptions.user import UserServiceException


async def get_user(request: Request, response: Response, user_service: UserServiceDep):
    try:
        user = await user_service.authentication(request=request, response=response)
        return user
    except UserServiceException:
        raise HTTPException(401, "Пользователь не зарегестрирован")

CurrentUserDep = Annotated[UserDTO, Depends(get_user)]


async def get_admin(user: CurrentUserDep):
    if user.role != "admin":
        print("Тут")
        input()
        raise HTTPException(status_code=500)
    return user


AdminDep = Annotated[UserDTO, Depends(get_admin)]