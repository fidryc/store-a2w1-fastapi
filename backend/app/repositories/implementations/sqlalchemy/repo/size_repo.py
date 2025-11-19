from app.db.models.models import Size
from app.repositories.implementations.sqlalchemy.base_repo import BaseSQLAlchemyRepository
from app.schemas.dto import SizeDTO

class SizeRepository(BaseSQLAlchemyRepository[SizeDTO, Size]):
    model = Size