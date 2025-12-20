from typing import Any, Protocol

from app.schemas.dto import CollectionCategoryDTO, CollectionDTO, ProductDTO
from app.schemas.filters import CollectionCategoryFilters


class ICollectionService(Protocol):
    async def products_by_collection_id(self, collection_id: int, desc=False) -> list[ProductDTO]: ...
            
    async def collection_by_id(self, collection_id) -> CollectionDTO | None: ...
    
    async def collections_by_cat_id(self, cat_id: id) -> list[CollectionDTO]: ...
    
    async def collection_categories_by_filters(self, filters: CollectionCategoryFilters) -> list[CollectionCategoryDTO]: ...