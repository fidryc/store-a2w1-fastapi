from app.services.interfaces.abc_collection_sertice import ICollectionService
from app.schemas.dto import CollectionCategoryDTO
from app.schemas.filters import CollectionCategoryFilters
from app.application.responsens.base_page import BasePageResponse
from app.constants.db import CollectionCategorySlug

class BasePageService:
    def __init__(self, collection_service: ICollectionService):
        self.collection_service = collection_service
        
    async def _get_collection_category(self, slug: str) -> CollectionCategoryDTO | None:
        categories = await self.collection_service.collection_categories_by_filters(
            CollectionCategoryFilters.model_construct(
                slug=slug,
                check_fields=False
            )
        )
        return categories[0] if categories else None

    async def get_home_page_data(self) -> BasePageResponse:
        large_category = await self._get_collection_category(CollectionCategorySlug.COLLECTION)
        capsule_category = await self._get_collection_category(CollectionCategorySlug.CAPSULE)

        data = {
            "large_category": large_category,
            "collections_of_large_category": (
                await self.collection_service.collections_by_cat_id(cat_id=large_category.id)
            ),
            "capsule_category": capsule_category,
            "collections_of_capsule_category": (
                await self.collection_service.collections_by_cat_id(cat_id=capsule_category.id)
            )
        }

        return BasePageResponse.model_construct(**data)
    
    
        
    