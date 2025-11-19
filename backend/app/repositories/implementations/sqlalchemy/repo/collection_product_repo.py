from app.db.models.models import CollectionProduct
from app.repositories.implementations.sqlalchemy.base_repo import BaseSQLAlchemyRepository
from app.schemas.dto import CollectionProductDTO

class CollectionProductRepository(BaseSQLAlchemyRepository[CollectionProductDTO, CollectionProduct]):
    model = CollectionProduct