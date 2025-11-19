from app.db.models.models import Collection
from app.repositories.implementations.sqlalchemy.base_repo import BaseSQLAlchemyRepository
from app.schemas.dto import CollectionDTO

class CollectionRepository(BaseSQLAlchemyRepository[CollectionDTO, Collection]):
    model = Collection