from app.repositories.interfaces.abc_base_uow import IBaseUOW
from app.schemas.dto import ProductDTO
from app.services.interfaces.abc_product_service import IProductService


class ProductService(IProductService):
    def __init__(self, uow: IBaseUOW):
        self.uow = uow
        
    async def get_product_by_id(self, id: int, desc_photo=False) -> ProductDTO:
        """Получение продукта по id"""
        products = await self.uow.product_repo.products_with_photo_by_filters(id=id)
        if not products:
            return None
        sizes = await self.uow.product_variant_repo.size_variation_of_product(product_id=id)
        product = products[0]
        product.photos = sorted(product.photos, key=lambda x: x.sort_order, reverse=desc_photo)
        return {"product": product, "sizes": sizes}