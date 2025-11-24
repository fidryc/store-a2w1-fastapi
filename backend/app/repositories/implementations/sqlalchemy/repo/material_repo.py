from app.db.models.models import Material
from app.repositories.implementations.sqlalchemy.base_repo import BaseSQLAlchemyRepository
from app.schemas.dto import MaterialDTO
from app.repositories.interfaces.abc_repo.abc_material_repo import IMaterialRepository

class MaterialRepository(IMaterialRepository, BaseSQLAlchemyRepository[MaterialDTO, Material]):
    model = Material