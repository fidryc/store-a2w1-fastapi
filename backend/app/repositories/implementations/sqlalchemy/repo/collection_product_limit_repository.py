from app.db.models.models import CollectionProductLimit
from app.repositories.implementations.sqlalchemy.base_repo import BaseSQLAlchemyRepository
from app.schemas.dto import CollectionProductLimitDTO
from app.repositories.interfaces.abc_repo.abc_collection_product_limit_repo import ICollectionProductLimitRepository

class CollectionProductLimitRepository(
    ICollectionProductLimitRepository,
    BaseSQLAlchemyRepository[CollectionProductLimitDTO, CollectionProductLimit]
):
    model = CollectionProductLimit
