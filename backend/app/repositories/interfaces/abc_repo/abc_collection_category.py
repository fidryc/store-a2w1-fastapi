from typing import Any, TypeVar
from app.repositories.interfaces.abc_base_repo import IBaseRepository

DTO = TypeVar("DTO")
Model = TypeVar("MODEL")

class ICollectionCategoryRepository(IBaseRepository[DTO, Model]): ...