from app.repositories.interfaces.abc_base_uow import IBaseUOW
from app.schemas.dto import CollectionCategoryDTO, CollectionDTO, CollectionWithDetailsDTO, ProductDTO, ProductWithCategoriesDTO, ProductWithCollectionDTO, ProductWithPhotoDTO, SizeDTO
from app.services.interfaces.abc_product_service import IProductService
from app.repositories.exceptions.base_exc import RepositoryExc
from app.core.logger import logger
from app.services.exceptions.product import ProductServiceException
from app.services.interfaces.abc_collection_sertice import ICollectionService
from app.schemas.filters import CollectionCategoryFilters
from app.services.exceptions.collection import CollectionServiceException


class ProductService(IProductService):
    def __init__(self, uow: IBaseUOW, collection_service: ICollectionService):
        self.uow = uow
        self.collection_service = collection_service
        
    async def product_with_details(
        self,
        id: int,
        desc_photo=False
    ) -> dict[str, ProductWithPhotoDTO | list[SizeDTO] | CollectionWithDetailsDTO | None]:
        """Получение продукта с фото, с возможными вариантами размеров, с коллекцией"""
        try:
            products = await self.uow.product_repo.products_with_photo_by_filters(id=id)
        except RepositoryExc as e:
            raise ProductServiceException("Ошибка получение продукта с фото", status_code=500) from e
        if not products:
            return {"product": None, "sizes": None}
        
        try:
            sizes = await self.uow.product_variant_repo.size_variation_of_product(product_id=id)
        except RepositoryExc as e:
            raise ProductServiceException("Ошибка получение продукта с фото", status_code=500) from e
        
        product = products[0]
        
        if product.collection_id:
            try:
                collection = await self.collection_service.collection_by_id(collection_id=product.collection_id)
            except CollectionServiceException as e:
                raise ProductServiceException("Ошибка получение коллекции продукта", status_code=500) from e
        product.photos = sorted(product.photos, key=lambda x: x.sort_order, reverse=desc_photo)
        return {"product": product, "sizes": sizes, "collection": collection}
    
    async def products_by_base_category_slug(self, slug: str) -> list[ProductWithCategoriesDTO]:
        """Получение всех товаров по slug базовой категории. 
        Сначала получаю id базовой категории, а после него получаю уже товары.
        Это сделано, чтобы не делать join для продуктов"""
        try:
            base_categories = await self.uow.base_category_repo.get_by_filters(
                slug=slug
            )
        except RepositoryExc as e:
            raise ProductServiceException("Ошибка получение продукта с фото", status_code=500) from e
        
        if not base_categories:
            return []
        
        try:
            products = await self.uow.product_repo.products_with_categories_by_filters(
                base_category_id=base_categories[0].id
            )
            return products
        except RepositoryExc as e:
            raise ProductServiceException("Ошибка получение продукта с фото", status_code=500) from e
        
    async def all_products(self) -> list[ProductWithCollectionDTO]:
        products = await self.uow.product_repo.products_with_collection()
        return products