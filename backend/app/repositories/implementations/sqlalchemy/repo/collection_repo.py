from sqlalchemy import select
from sqlalchemy.orm import joinedload
from typing import Any
from app.db.models.models import Collection
from app.repositories.implementations.sqlalchemy.base_repo import BaseSQLAlchemyRepository
from app.schemas.dto import CollectionDTO
from app.repositories.interfaces.abc_repo.abc_collection_repo import ICollectionRepository
from app.db.models.models import Photo

class CollectionRepository(ICollectionRepository, BaseSQLAlchemyRepository[CollectionDTO, Collection]):
    model = Collection
    
    async def collections_with_category_and_photo(self) -> list[tuple[Any]]:
        query = select(self.model).options(joinedload(self.model.photo),  joinedload(self.model.collection_category))
        result = await self.session.execute(query)
        return [self.model.serialize_to_dto(model) for model in result.scalars().all()]