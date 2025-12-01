from typing import Any
from venv import logger
from app.repositories.exceptions.base_exc import RepositoryExc
from app.repositories.interfaces.abc_base_uow import IBaseUOW
from app.schemas.dto import CollectionDTO, ProductDTO
from app.services.exceptions.collection import CollectionServiceException
from app.services.interfaces.abc_product_service import IProductService
from app.services.interfaces.abc_collection_sertice import ICollectionService
from fastapi import status


class CollectionService(ICollectionService):
    def __init__(self, uow: IBaseUOW, product_service: IProductService):
        self.uow = uow
        self.product_service = product_service

    
    async def all_collections_with_photo(
        self, **filters
    ) -> list[CollectionDTO]:
        """Получение всех коллекций с их photo relationship"""
        collections = await self.uow.collection_repo.collections_with_category_and_photo(**filters)
        return collections
    
    async def _collections_with_category_and_photo(
        self
    ) -> list[CollectionDTO]:
        collections = await self.uow.collection_repo.collections_with_category_and_photo()
        return collections
    
    async def categories_with_collections(self) -> list[tuple[Any, list[Any]]]:
        """Получение list из tuple где в первом элементе лежит категория коллекции, а вторым - все коллекции категории"""
        cl_with_cat_and_photo = await self._collections_with_category_and_photo()
        cl_with_cat_and_photo.sort(key=lambda x: x.collection_category.sort_order)
        res = {}
        for collection in cl_with_cat_and_photo:
            id_col_cats = collection.collection_category.id
            res[id_col_cats] = res.get(id_col_cats, (collection.collection_category, []))
            res[id_col_cats][1].append(collection)
        return [res[k] for k, v in res.items()]
    
    async def get_products_by_collection_id(self, collection_id: int, desc=False) -> list[ProductDTO]:
        """Получение всех продуктов по id коллекции"""
        products = await self.uow.product_repo.products_with_photo_by_filters(collection_id=collection_id)
        return products
    
    async def get_collection_by_id(self, collection_id) -> CollectionDTO | None:
        """Получение коллекции по id"""
        try:
            collection = await self.uow.collection_repo.collections_with_category_and_photo(id=collection_id)
        except RepositoryExc as e:
            logger.warning(
                "Failed get collection by id",
                extra={
                    "collection_category_id": collection_id
                },
                exc_info=True
            )
            raise CollectionServiceException(
                "Ошибка получения коллекции",
                status_code=status.HTTP_404_NOT_FOUND
            ) from e
            
        if not collection:
            raise CollectionServiceException(
                "Коллекция не найдена по id",
                status_code=status.HTTP_404_NOT_FOUND
            )
        return collection[0]