from typing import TypeVar
from app.repositories.interfaces.abc_base_repo import IBaseRepository
from app.schemas.dto import ProductWithCategoriesDTO, ProductWithCollectionDTO, ProductWithPhotoDTO

DTO = TypeVar("DTO")
Model = TypeVar("MODEL")

class IProductRepository(IBaseRepository[DTO, Model]):
    async def products_with_photo_by_filters(self, **filters) -> list[ProductWithPhotoDTO]: ...
    
    async def products_with_categories_by_filters(self, **filters) -> ProductWithCategoriesDTO: ...
    
    async def products_with_collection(self, **filters) -> list[ProductWithCollectionDTO]: ...
