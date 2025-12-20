from pydantic import BaseModel

class CollectionCategoryFilters(BaseModel):
    id: int | None = None
    title: str | None = None
    description: str | None = None
    sort_order: int | None = None