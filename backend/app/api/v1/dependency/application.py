from typing import Annotated
from fastapi import Depends

from app.application.services.base_page import BasePageService
from app.api.v1.dependency.uow import UOWDep
from app.services.implementations.collection_service import CollectionService


async def get_base_page_service(uow: UOWDep) -> BasePageService:
    return BasePageService(
        collection_service=CollectionService(
            uow=uow
        )
    )
    
    
BasePageServiceDep = Annotated[BasePageService, Depends(get_base_page_service)]