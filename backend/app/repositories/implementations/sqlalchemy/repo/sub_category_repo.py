from app.db.models.models import SubCategory
from app.repositories.implementations.sqlalchemy.base_repo import BaseSQLAlchemyRepository
from app.schemas.dto import SubCategoryDTO
from app.repositories.interfaces.abc_repo.abc_sub_category_repo import ISubCategoryRepository

class SubCategoryRepository(ISubCategoryRepository, BaseSQLAlchemyRepository[SubCategoryDTO, SubCategory]):
    model = SubCategory