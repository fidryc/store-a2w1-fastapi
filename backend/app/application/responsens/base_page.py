from typing import Optional
from pydantic import BaseModel
from app.schemas.dto import CollectionCategoryDTO, CollectionDTO, BaseCategoryDTO

class BasePageResponse(BaseModel):
    large_category: Optional[CollectionCategoryDTO] = None
    collections_of_large_category: Optional[list[CollectionDTO]] = None
    capsule_category: Optional[CollectionCategoryDTO] = None
    collections_of_capsule_category: Optional[list[CollectionDTO]]= None