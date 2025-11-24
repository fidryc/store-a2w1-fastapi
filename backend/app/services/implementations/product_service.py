from app.repositories.interfaces.abc_base_uow import IBaseUOW
from app.schemas.dto import ProductDTO
from app.services.interfaces.abc_product_service import IProductService


class ProductService(IProductService):
    def __init__(self, uow: IBaseUOW):
        self.uow = uow
        
    async def get_all_products(self, ids: list[int]) -> list[ProductDTO]:
        products = []
        for id in ids:
            product = await self.uow.product_repo.get_by_id(id=id)
            products.append(product)
        return products