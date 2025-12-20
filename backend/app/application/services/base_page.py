from app.repositories.interfaces.abc_base_uow import IBaseUOW
from app.services.interfaces.abc_collection_sertice import ICollectionService
from app.application.exception.base import ApplicationServiceException, ApplicationServiceException
from app.schemas.dto import CollectionCategoryDTO
from app.schemas.filters import CollectionCategoryFilters
from app.application.responsens.base_page import BasePageResponse
from app.repositories.exceptions.base_exc import RepositoryExc


class TableNames:
    LARGE_CATEGORY_COLLECTION = "Коллекция"
    CAPSULE_CATEGORY_COLLECTION  = "Капсульная коллекция"
    ATRIBUTICES_BASE_CATEGORY = "Постеры/Стикеры"

class BasePageService:
    def __init__(self, uow: IBaseUOW, collection_service: ICollectionService):
        self.uow = uow
        self.collection_service = collection_service
        
    async def _get_category(self, title: str) -> CollectionCategoryDTO | None:
        categories = await self.collection_service.collection_categories_by_filters(
            CollectionCategoryFilters.model_construct(
                title=title,
                check_fields=False
            )
        )
        return categories[0] if categories else None

    async def _get_collections(self, category: CollectionCategoryDTO):
        return await self.collection_service.collections_by_cat_id(cat_id=category.id)

    async def get_home_page_data(self) -> BasePageResponse:
        large_category = await self._get_category(TableNames.LARGE_CATEGORY_COLLECTION)
        capsule_category = await self._get_category(TableNames.CAPSULE_CATEGORY_COLLECTION)

        try:
            stickers_posters = await self.uow.base_category_repo.get_by_filters(title=TableNames.ATRIBUTICES_BASE_CATEGORY)
        except RepositoryExc as e:
            raise ApplicationServiceException("Ошибка получения постеров", status_code=500)
        data = {
            "large_category": large_category,
            "collections_of_large_category": (
                await self._get_collections(large_category) if large_category else []
            ),
            "capsule_category": capsule_category,
            "collections_of_capsule_category": (
                await self._get_collections(capsule_category) if capsule_category else []
            ),
            "stickers_posters": stickers_posters if stickers_posters else None
        }

        return BasePageResponse.model_construct(**data)
    
    
        
    