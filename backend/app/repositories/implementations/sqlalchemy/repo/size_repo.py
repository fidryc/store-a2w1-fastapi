from typing import Any
from sqlalchemy import text
from app.db.models.models import Size
from app.repositories.implementations.sqlalchemy.base_repo import BaseSQLAlchemyRepository
from app.schemas.dto import SizeDTO
from app.repositories.interfaces.abc_repo.abc_size_repo import ISizeRepository

class SizeRepository(ISizeRepository, BaseSQLAlchemyRepository[SizeDTO, Size]):
    model = Size