from typing import TypeVar

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import insert, select

from app.db.models.models import Base
from app.repositories.interfaces.abc_base_repo import IBaseRepository

DTO = TypeVar("DTO", bound=BaseModel)
Model = TypeVar("MODEL", bound=Base)

class BaseSQLAlchemyRepository(IBaseRepository[DTO, Model]):
    model: Model
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_by_id(self, id: int) -> DTO:
        query = select(self.model).where(self.model.id == id)
        obj = (await self.session.execute(query)).scalar_one_or_none()
        return self.model.serialize_to_dto(obj)
    
    async def get_all(self) -> list[DTO]:
        query = select(self.model)
        objs = (await self.session.execute(query)).scalars().all()
        return [self.model.serialize_to_dto(obj) for obj in objs]
    
    async def add(self, obj: dict) -> int:
        query = insert(self.model).values(**obj).returning(self.model.id)
        id = (await self.session.execute(query)).scalar_one_or_none()
        return id