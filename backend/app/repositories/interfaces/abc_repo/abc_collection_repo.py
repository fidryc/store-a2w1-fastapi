from typing import Any, TypeVar
from app.repositories.interfaces.abc_base_repo import IBaseRepository

DTO = TypeVar("DTO")
Model = TypeVar("MODEL")

class ICollectionRepository(IBaseRepository[DTO, Model]):
    async def collections_with_category_and_photo(self, **filters) -> list[tuple[Any]]:
        ...
