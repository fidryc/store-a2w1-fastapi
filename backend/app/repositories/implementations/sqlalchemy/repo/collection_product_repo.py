from sqlalchemy import text
from app.db.models.models import CollectionProduct
from app.repositories.implementations.sqlalchemy.base_repo import BaseSQLAlchemyRepository
from app.schemas.dto import CollectionProductDTO
from app.repositories.interfaces.abc_repo.abc_collection_product_repo import ICollectionProductRepository

class CollectionProductRepository(
    ICollectionProductRepository,
    BaseSQLAlchemyRepository[CollectionProductDTO, CollectionProduct]
):
    model = CollectionProduct
    