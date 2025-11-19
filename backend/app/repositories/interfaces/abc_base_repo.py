from typing import Any, Protocol, Generic, TypeVar

DTO = TypeVar("DTO")
Model = TypeVar("MODEL")

class IBaseRepository(Protocol, Generic[DTO, Model]):
    model: Model
    
    def __init__(self, session: Any):
        self.session = session
        
    async def get_by_id(self, id: int) -> DTO: ...
    
    async def get_all(self, ) -> list[DTO]: ...
    
    async def add(self, obj: dict) -> int: ...