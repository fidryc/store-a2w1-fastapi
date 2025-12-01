from typing import Any
from app.core.logger import logger
from app.services.implementations.collection_service import CollectionService
from app.services.implementations.product_service import ProductService
from app.schemas.dto import CollectionDTO
from app.repositories.interfaces.abc_base_uow import IBaseUOW
from app.repositories.exceptions.base_exc import RepositoryExc
from app.services.exceptions.base import ServiceException


class FrontendBaseService:
    def __init__(self, uow: IBaseUOW, collection_service: CollectionService):
        self.collection_service = collection_service
        self.uow = uow
        
    async def base_data(self) -> dict[str, tuple[Any, list[CollectionDTO]]]:
        """Разбивка на коллекции / капсула  для формирования header footer"""
        try:
            large_collection = await self.uow.collection_category_repo.get_by_filters(title="Коллекция")
            capsule = await self.uow.collection_category_repo.get_by_filters(title="Капсульная коллекция")
        except RepositoryExc as e:
            logger.critical(
                msg="Collection category repository error",
                exc_info=True
            )
            raise ServiceException("Ошибка получения данных по категория коллекций", argsstatus_code=500) from e
        
        if not large_collection or not capsule:
            raise ServiceException("Не существует такой категории коллекций", argsstatus_code=409)
        res = {
            "large_collection": (large_collection[0], []),
            "capsule": (capsule[0], [])
        }
        cats_cols = await self.collection_service.categories_with_collections()
        for cat, cols in cats_cols:
            if cat.title == "Капсульная коллекция":
                res["capsule"][1].extend(cols)
            elif cat.title == "Коллекция":
                res["large_collection"][1].extend(cols)
        return res