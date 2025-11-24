from typing import TypeVar

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import delete, insert, select
from sqlalchemy.exc import SQLAlchemyError

from app.db.models.models import Base
from app.repositories.interfaces.abc_base_repo import IBaseRepository
from app.repositories.exceptions.base_exc import RepositoryExc
from app.core.logger import logger

DTO = TypeVar("DTO", bound=BaseModel)
Model = TypeVar("MODEL", bound=Base)

class BaseSQLAlchemyRepository(IBaseRepository[DTO, Model]):
    model: Model
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_by_id(self, id: int) -> DTO:
        try:
            query = select(self.model).where(self.model.id == id)
            obj = (await self.session.execute(query)).scalar_one_or_none()
            return self.model.serialize_to_dto(obj)
        except SQLAlchemyError as e:
            logger.warning(
                "SQLAlchemyError: failed get by id",
                exc_info=True,
                extra={"id": id}
                )
            raise RepositoryExc("Failed get by id") from e
    
    async def get_all(self) -> list[DTO]:
        try:
            query = select(self.model)
            objs = (await self.session.execute(query)).scalars().all()
            return [self.model.serialize_to_dto(obj) for obj in objs]
        except SQLAlchemyError as e:
            logger.warning(
                "SQLAlchemyError: failed get all",
                exc_info=True,
                )
            raise RepositoryExc("Failed get all") from e
    
    async def add(self, obj: dict) -> int:
        try:
            query = insert(self.model).values(**obj).returning(self.model.id)
            id = (await self.session.execute(query)).scalar_one_or_none()
            return id
        except SQLAlchemyError as e:
            logger.warning(
                "SQLAlchemyError: failed add",
                exc_info=True,
                extra={"obj": obj}
                )
            raise RepositoryExc("Failed get add") from e
        
    async def get_by_filters(self, **filters) -> list[DTO]:
        try:
            query = select(self.model).where(*[getattr(self.model, k) == v for k, v in filters.items()])
            objs = (await self.session.execute(query)).scalars().all()
            return [self.model.serialize_to_dto(obj) for obj in objs]
        except SQLAlchemyError as e:
            logger.warning(
                "SQLAlchemyError: failed get by filters",
                exc_info=True,
                extra={"filters": filters}
                )
            raise RepositoryExc("Failed get by filters") from e
        
    async def delete_by_filters(self, **filters) -> list[int]:
        try:
            query = delete(self.model).where(*[getattr(self.model, k) == v for k, v in filters.items()]).returning(self.model.id)
            ids = (await self.session.execute(query)).scalars().all()
            return ids
        except SQLAlchemyError as e:
            logger.warning(
                "SQLAlchemyError: failed delete by filters",
                exc_info=True,
                extra={"filters": filters}
                )
            raise RepositoryExc("Failed delete by filters") from e