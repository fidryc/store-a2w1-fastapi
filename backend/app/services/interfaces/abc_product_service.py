from typing import Protocol
from app.schemas.dto import ProductDTO


class IProductService(Protocol):
    async def get_product_by_id(self, id: int, desc_photo=False) -> ProductDTO: ...