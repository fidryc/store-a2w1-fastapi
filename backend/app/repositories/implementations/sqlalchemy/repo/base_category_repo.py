from app.db.models.models import BaseCategory
from app.repositories.implementations.sqlalchemy.base_repo import BaseSQLAlchemyRepository
from app.schemas.dto import BaseCategoryDTO
from app.repositories.interfaces.abc_repo.abc_base_category_repo import IBaseCategoryRepository

class BaseCategoryRepository(IBaseCategoryRepository, BaseSQLAlchemyRepository[BaseCategoryDTO, BaseCategory]):
    model = BaseCategory