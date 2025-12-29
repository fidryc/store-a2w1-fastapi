from typing import Any, Protocol

from app.schemas.dto import CollectionCategoryDTO, CollectionDTO, CollectionProductLimitDTO, CollectionWithDetailsDTO, ProductWithCategoriesDTO, ProductWithPhotoDTO
from app.schemas.filters import CollectionCategoryFilters, CollectionFilters


class ICollectionService(Protocol):
    async def products_by_collection_id(
        self,
        collection_id: int,
        is_photos_sort=False,
        photos_sort_desc=True
    ) -> list[ProductWithCategoriesDTO]: ...
            
    async def collection_by_id(self, collection_id) -> CollectionWithDetailsDTO | None: ...
    
    async def collection_by_filters(self, filters: CollectionFilters) -> list[CollectionDTO]: ...
    
    async def collection_base_category_limit(
        self,
        collection_id: int,
        base_category_id: int
    ) -> CollectionProductLimitDTO | None: ...
    
    async def collections_by_cat_id(self, cat_id: id) -> list[CollectionWithDetailsDTO]: ...
    
    async def collection_categories_by_filters(self, filters: CollectionCategoryFilters) -> list[CollectionCategoryDTO]: ...
    