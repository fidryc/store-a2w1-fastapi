from app.db.models.models import BaseCategory
from app.repositories.implementations.sqlalchemy.base_repo import BaseSQLAlchemyRepository
from app.schemas.dto import BaseCategoryDTO

class BaseCategoryRepository(BaseSQLAlchemyRepository[BaseCategoryDTO, BaseCategory]):
    model = BaseCategory