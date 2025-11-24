from typing import Protocol
from app.schemas.dto import ProductDTO


class IProductService(Protocol):
    async def get_all_products(self, ids: list[int]) -> list[ProductDTO]: ...