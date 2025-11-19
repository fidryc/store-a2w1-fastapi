from typing import TypeVar
from app.repositories.interfaces.abc_base_repo import IBaseRepository

DTO = TypeVar("DTO")
Model = TypeVar("MODEL")

class ISubCategoryRepository(IBaseRepository[DTO, Model]):
    ...
