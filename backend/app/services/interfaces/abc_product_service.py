from typing import Protocol
from app.schemas.dto import CollectionDTO, ProductDTO, ProductWithCategoriesDTO, ProductWithPhotoDTO, SizeDTO


class IProductService(Protocol):
    async def product_with_details(
        self,
        id: int,
        desc_photo=False
    ) -> dict[str, ProductWithPhotoDTO | list[SizeDTO] | CollectionDTO | None]:
        """Получение продукта с фото, с возможными вариантами размеров, с коллекцией"""
        ...
    
    async def products_by_base_category_slug(self, base_category_slug: str) -> list[ProductWithCategoriesDTO]: ...