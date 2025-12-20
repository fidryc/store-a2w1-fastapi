from typing import Any, TypeVar
from app.repositories.interfaces.abc_base_repo import IBaseRepository
from app.schemas.dto import ColorDTO, SizeDTO

DTO = TypeVar("DTO")
Model = TypeVar("MODEL")

class IProductVariantRepository(IBaseRepository[DTO, Model]):
    async def size_variation_of_product(self, product_id: int)  -> list[SizeDTO]: ...
    
    async def color_variation_of_product(self, product_id: int) -> list[ColorDTO]: ...
    
    