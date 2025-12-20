from pydantic import BaseModel
from app.schemas.dto import CollectionCategoryDTO, CollectionDTO, BaseCategoryDTO

class BasePageResponse(BaseModel):
    large_category: CollectionCategoryDTO | None = None
    collections_of_large_category: list[CollectionDTO] | None = None
    capsule_category: CollectionCategoryDTO | None = None
    collections_of_capsule_category: list[CollectionDTO] | None = None
    stickers_posters: BaseCategoryDTO | None = None