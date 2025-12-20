from app.repositories.interfaces.abc_base_uow import IBaseUOW
from app.services.interfaces.abc_collection_sertice import ICollectionService
from app.application.responsens.collections_page import CollectionsByCatIdPageResponse

class CollectionsPageService:
    def __init__(self, collection_service: ICollectionService):
        self.collection_service = collection_service
        
        
    async def get_collections_by_cat_id_page_data(self, collection_category_id: int) -> CollectionsByCatIdPageResponse:
        collections = await self.collection_service.collections_by_cat_id(
            cat_id=collection_category_id
        )
        return CollectionsByCatIdPageResponse.model_construct(
            collections=collections
        )
        
    async def get_collection_by_id_page_data(self, collection_id: int):
        collections = await self.collection_service.collection_by_id(
            collection_id=collection_id
        )
        mapped_by_cat = {}
        