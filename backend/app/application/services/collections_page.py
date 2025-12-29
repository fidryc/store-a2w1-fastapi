from app.repositories.interfaces.abc_base_uow import IBaseUOW
from app.services.interfaces.abc_collection_sertice import ICollectionService
from app.application.responsens.collections_page import CollectionByIdPageResponse, CollectionsByCatIdPageResponse, GroupedByBaseCategory, PostersAndStickersPageResponse
from app.constants.constants import BaseCategorySlug
from app.schemas.dto import ProductWithCategoriesDTO
from app.services.interfaces.abc_product_service import IProductService

class CollectionsPageService:
    def __init__(self, collection_service: ICollectionService, product_service: IProductService):
        self.collection_service = collection_service
        self.product_service = product_service
        
    async def get_collections_by_cat_id_page_data(self, collection_category_id: int) -> CollectionsByCatIdPageResponse:
        collections = await self.collection_service.collections_by_cat_id(cat_id=collection_category_id)
        return CollectionsByCatIdPageResponse.model_construct(
            collections=collections
        )
        
        
        
    async def get_collection_by_id_page_data(self, collection_id: int) -> CollectionByIdPageResponse:
        collection = await self.collection_service.collection_by_id(collection_id=collection_id)
        products = await self.collection_service.products_by_collection_id(collection_id=collection_id)
        
        print(collection)
        print(products)
        
        grouped = await self._group_products_by_base_cat(
            products=products,
            collection_id=collection_id  # Получаем лимиты
        )
        
        return CollectionByIdPageResponse.model_construct(
            collection=collection,
            grouped_by_base_category=grouped
        )

    # Для постеров/стикеров
    async def get_posters_and_stickers_page_data(self) -> PostersAndStickersPageResponse:
        posters = await self.product_service.products_by_base_category_slug(BaseCategorySlug.POSTERS)
        stickers = await self.product_service.products_by_base_category_slug(BaseCategorySlug.STICKERS)
        
        all_products = posters + stickers
        
        grouped = await self._group_products_by_base_cat(
            products=all_products,
            collection_id=None  # НЕ получаем лимиты → будет None
        )
        
        return PostersAndStickersPageResponse(
            grouped_by_base_category=grouped
        )

    # Универсальный метод группировки
    async def _group_products_by_base_cat(
        self,
        products: list[ProductWithCategoriesDTO],
        collection_id: int | None = None
    ) -> list[GroupedByBaseCategory]:
        """Разбиваю на продукты по категории и добавляю ограничение по количеству на категорию, если есть collection_id
        При collection_id = None -> limit_quantity остается None.
        None на стороне рендеринга страницы "groupes_by_category.html" воспринимается как "нет ограничений".
        Если collection_id будет передан, то вместо этого будет написано количество товаров на категорию внутри коллекции.
        
        Это сделано из-за того, что есть две одиннаковые страницы по внешнему виду для коллекции, где
        отображается ограничение категорий в зависимости от коллекции
        и просто для всех стикеров и постеров. Пока я придумал такое решение, но возможно поправлю в будущем.
        
        
        """
        groups = {}
        
        for product in products:
            cat_id = product.base_category_id
            
            if cat_id not in groups:
                groups[cat_id] = GroupedByBaseCategory(
                    base_category=product.base_category,
                    products=[],
                    limit_quantity=None
                )
            
            # Загружаем лимит только если передан collection_id
            if collection_id and groups[cat_id].limit_quantity is None:
                groups[cat_id].limit_quantity = (
                    await self.collection_service.collection_base_category_limit(
                        collection_id=collection_id,
                        base_category_id=cat_id
                    )
                )
            
            groups[cat_id].products.append(product)
        
        return list(groups.values())