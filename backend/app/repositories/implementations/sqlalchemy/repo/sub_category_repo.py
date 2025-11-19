from app.db.models.models import SubCategory
from app.repositories.implementations.sqlalchemy.base_repo import BaseSQLAlchemyRepository
from app.schemas.dto import SubCategoryDTO

class SubCategoryRepository(BaseSQLAlchemyRepository[SubCategoryDTO, SubCategory]):
    model = SubCategory