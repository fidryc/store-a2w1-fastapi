from typing import Any, Protocol

from app.schemas.dto import CollectionDTO, ProductDTO


class ICollectionService(Protocol):
    async def all_collections_with_photo(
        self
    ) -> list[CollectionDTO]: ...
            
    async def all_collections_with_products(
        self
        ) -> list[CollectionDTO]: ...
    
    async def categories_with_collections(self) -> dict[int: tuple[Any, list[Any]]]: ...
    
    async def get_products_by_collection_id(self, collection_id: int, desc=False) -> list[ProductDTO]: ...
    
    async def get_collection_by_id(self, collection_id) -> CollectionDTO | None: ...