from app.db.models.models import Color
from app.repositories.implementations.sqlalchemy.base_repo import BaseSQLAlchemyRepository
from app.schemas.dto import ColorDTO

class ColorRepository(BaseSQLAlchemyRepository[ColorDTO, Color]):
    model = Color