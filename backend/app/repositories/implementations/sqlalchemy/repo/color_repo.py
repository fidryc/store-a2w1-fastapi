from app.db.models.models import Color
from app.repositories.implementations.sqlalchemy.base_repo import BaseSQLAlchemyRepository
from app.schemas.dto import ColorDTO
from app.repositories.interfaces.abc_repo.abc_color_repo import IColorRepository

class ColorRepository(IColorRepository, BaseSQLAlchemyRepository[ColorDTO, Color]):
    model = Color
    