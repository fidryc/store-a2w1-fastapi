from typing import Protocol

from app.schemas.dto import CollectionDTO, ProductDTO


class ICollectionService(Protocol):
    async def collection_with_products(
        self,
        collection_id: int
        ) -> tuple[CollectionDTO, list[ProductDTO]]: ...
            
    async def all_collections_with_products(
        self
        ) -> list[CollectionDTO]: ...