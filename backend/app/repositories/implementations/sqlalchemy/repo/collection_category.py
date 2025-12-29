from app.db.models.models import CollectionCategory
from app.repositories.implementations.sqlalchemy.base_repo import BaseSQLAlchemyRepository
from app.repositories.interfaces.abc_repo.abc_collection_category import ICollectionCategoryRepository
from app.schemas.dto import CollectionCategoryDTO

class CollectionCategoryRepository(
    ICollectionCategoryRepository,
    BaseSQLAlchemyRepository[CollectionCategoryDTO, CollectionCategory]
):
    model = CollectionCategory
    