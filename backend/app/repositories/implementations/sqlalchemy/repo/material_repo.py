from app.db.models.models import Material
from app.repositories.implementations.sqlalchemy.base_repo import BaseSQLAlchemyRepository
from app.schemas.dto import MaterialDTO

class MaterialRepository(BaseSQLAlchemyRepository[MaterialDTO, Material]):
    model = Material