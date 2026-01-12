from typing import Protocol
from app.schemas.dto import CollectionDTO, ProductWithCategoriesDTO, ProductWithCollectionDTO, ProductWithPhotoDTO, SizeDTO


class IProductService(Protocol):
    async def product_with_details(
        self,
        id: int,
        desc_photo=False
    ) -> dict[str, ProductWithPhotoDTO | list[SizeDTO] | CollectionDTO | None]: ...
    
    async def products_by_base_category_slug(self, slug: str) -> list[ProductWithCategoriesDTO]: ...
    
    async def all_products(self) -> list[ProductWithCollectionDTO]: ...