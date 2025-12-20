from app.repositories.exceptions.base_exc import RepositoryExc
from app.repositories.interfaces.abc_base_uow import IBaseUOW
from app.schemas.dto import CollectionCategoryDTO, CollectionDTO, ProductDTO
from app.services.exceptions.collection import CollectionServiceException
from app.services.interfaces.abc_product_service import IProductService
from app.services.interfaces.abc_collection_sertice import ICollectionService
from fastapi import status

from app.schemas.filters import CollectionCategoryFilters


class CollectionService(ICollectionService):
    def __init__(self, uow: IBaseUOW):
        self.uow = uow

    # async def collections_with_photo(
    #     self, **filters
    # ) -> list[CollectionDTO]:
    #     """Получение всех коллекций с их photo relationship"""
    #     collections = await self.uow.collection_repo.collections_with_category_and_photo(**filters)
    #     return collections
    
    # async def categories_with_collections(self) -> list[tuple[CollectionCategoryDTO, list[CollectionDTO]]]:
    #     """Получение list из tuple где в первом элементе лежит категория коллекции, а вторым - все коллекции категории"""
    #     cl_with_cat_and_photo = await self.uow.collection_repo.collections_with_category_and_photo()
    #     cl_with_cat_and_photo.sort(key=lambda x: x.collection_category.sort_order)
    #     res = {}
    #     for collection in cl_with_cat_and_photo:
    #         id_col_cats = collection.collection_category.id
    #         res[id_col_cats] = res.get(id_col_cats, (collection.collection_category, []))
    #         res[id_col_cats][1].append(collection)
    #     return [res[k] for k, v in res.items()]
    
    async def products_by_collection_id(self, collection_id: int, desc=False) -> list[ProductDTO]:
        """Получение всех продуктов по id коллекции"""
        try:
            products = await self.uow.product_repo.products_with_photo_by_filters(collection_id=collection_id)
            return products
        except RepositoryExc as e:
            raise CollectionServiceException(
                "Ошибка получения коллекции",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            ) from e
    
    async def collection_by_id(self, collection_id) -> CollectionDTO | None:
        """Получение коллекции по id"""
        try:
            collection = await self.uow.collection_repo.collections_with_category_and_photo(id=collection_id)
        except RepositoryExc as e:
            raise CollectionServiceException(
                "Ошибка получения коллекции",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            ) from e
            
        if not collection:
            return None
        return collection[0]
    
    async def collections_by_cat_id(self, cat_id: int) -> list[CollectionDTO]:
        """Получение коллекций по id категории коллекции"""
        try:
            collections = await self.uow.collection_repo.collections_with_category_and_photo(
                collection_category_id=cat_id
            )
            return collections
        except RepositoryExc as e:
            raise CollectionServiceException(
                "Ошибка получения коллекций",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            ) from e
    
    async def collection_categories_by_filters(self, filters: CollectionCategoryFilters) -> list[CollectionCategoryDTO]:
        """Получение категории коллекции по фильтрам"""
        try:
            collection_categories = await self.uow.collection_category_repo.get_by_filters(
                **filters.model_dump(exclude_none=True)
            )
            return collection_categories
        except RepositoryExc as e:
            raise CollectionServiceException(
                "Ошибка получения категории коллекции по фильтрам",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            ) from e