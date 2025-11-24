from typing import Annotated

from fastapi import Depends
from app.repositories.implementations.sqlalchemy.base_uow import BaseUOW


async def get_uow():
    async with BaseUOW() as uow:
        yield uow
        

UOWDep = Annotated[BaseUOW, Depends(get_uow)]