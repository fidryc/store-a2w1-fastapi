from app.repositories.exceptions.base_exc import RepositoryExc
from app.repositories.interfaces.abc_base_uow import IBaseUOW
from app.schemas.dto import CollectionCategoryDTO, CollectionDTO, CollectionProductLimitDTO, CollectionWithDetailsDTO, ProductDTO, ProductWithCategoriesDTO, ProductWithPhotoDTO
from app.services.exceptions.collection import CollectionServiceException
from app.services.interfaces.abc_product_service import IProductService
from app.services.interfaces.abc_collection_sertice import ICollectionService
from fastapi import status

from app.schemas.filters import CollectionCategoryFilters, CollectionFilters


class CollectionService(ICollectionService):
    def __init__(self, uow: IBaseUOW):
        self.uow = uow
    
    async def products_by_collection_id(
        self,
        collection_id: int,
        is_photos_sort=False,
        photos_sort_desc=True
        ) -> list[ProductWithCategoriesDTO]:
        """Получение всех продуктов по id коллекции"""
        try:
            products = await self.uow.product_repo.products_with_categories_by_filters(
                collection_id=collection_id
            )
        except RepositoryExc as e:
            raise CollectionServiceException(
                "Ошибка получения коллекции",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            ) from e
            
        if is_photos_sort:
            products.photos.sort(key=lambda product_photo: product_photo.photo, reverse=photos_sort_desc)

        return products
        
    async def collection_by_id(self, collection_id: int) -> CollectionWithDetailsDTO | None:
        """Получение коллекции по id"""
        try:
            collection = await self.uow.collection_repo.collections_with_category_and_photo(
                id=collection_id
            )
        except RepositoryExc as e:
            raise CollectionServiceException(
                "Ошибка получения коллекции",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            ) from e
            
        if not collection:
            return None
        return collection[0]
    
    async def collection_by_filters(self, filters: CollectionFilters) -> list[CollectionDTO]:
        """Получение коллекции по фильтрам"""
        try:
            collections = await self.uow.collection_repo.get_by_filters(**filters.model_dump(exclude_none=True))
            return collections
        except RepositoryExc as e:
            raise CollectionServiceException(
                "Ошибка получения коллекции",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            ) from e
            
    
    async def collection_base_category_limit(
        self,
        collection_id: int,
        base_category_id: int
    ) -> CollectionProductLimitDTO | None:
        """
        Получение ограничение количества товаров по категори
        
        0 - Ограничений нет
        """
        try:
            collection_limits = await self.uow.collection_product_limit_repo.get_by_filters(
                collection_id=collection_id,
                base_category_id=base_category_id
            )
        except RepositoryExc as e:
            raise CollectionServiceException(
                "Ошибка получения ограничение категории в коллекции",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            ) from e
            
        return collection_limits[0] if collection_limits else None
            
    
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