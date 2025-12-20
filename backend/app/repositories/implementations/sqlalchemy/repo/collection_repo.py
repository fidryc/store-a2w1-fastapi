from sqlalchemy import select
from sqlalchemy.orm import joinedload
from typing import Any
from sqlalchemy.dialects import postgresql
from app.db.models.models import Collection
from app.repositories.implementations.sqlalchemy.base_repo import BaseSQLAlchemyRepository
from app.schemas.dto import CollectionDTO, CollectionWithDetailsDTO
from app.repositories.interfaces.abc_repo.abc_collection_repo import ICollectionRepository
from app.repositories.utils.serializer import Serializer

class CollectionRepository(ICollectionRepository, BaseSQLAlchemyRepository[CollectionDTO, Collection]):
    model = Collection
    
    async def collections_with_category_and_photo(self, **filters) -> list[CollectionWithDetailsDTO]:
        query = select(
            self.model
        ).where(
            *[getattr(self.model, k) == v for k, v in filters.items()]
        ).options(
            joinedload(self.model.photo),
            joinedload(self.model.collection_category)
        )
        result = await self.session.execute(query)
        return [Serializer.serialize_to_dto(CollectionWithDetailsDTO, model) for model in result.scalars().all()]