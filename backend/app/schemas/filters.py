from typing import Optional
from pydantic import BaseModel

class CollectionCategoryFilters(BaseModel):
    id: int | None = None
    title: str | None = None
    slug: str | None = None
    description: str | None = None
    sort_order: int | None = None
    

class CollectionFilters(BaseModel):
    id: int | None = None
    title: str | None = None
    description: str | None = None