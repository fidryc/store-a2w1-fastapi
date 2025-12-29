from pydantic import BaseModel, ConfigDict, Field
from app.schemas.dto import (
    BaseCategoryDTO, 
    CollectionDTO, 
    CollectionProductLimitDTO,
    CollectionWithDetailsDTO, 
    ProductWithPhotoDTO
)
from typing import Optional


class CollectionsByCatIdPageResponse(BaseModel):
    """Список коллекций по ID категории коллекций"""
    collections: list[CollectionWithDetailsDTO] = Field(default_factory=list)


class GroupedByBaseCategory(BaseModel):
    """Товары, сгруппированные по базовой категории"""
    base_category: Optional[BaseCategoryDTO] = None
    products: Optional[list[ProductWithPhotoDTO]] = []
    limit_quantity: Optional[CollectionProductLimitDTO] = None  # Может отсутствовать


class CollectionByIdPageResponse(BaseModel):
    """Страница конкретной коллекции с товарами"""
    collection: CollectionDTO
    grouped_by_base_category: list[GroupedByBaseCategory] = Field(
        default_factory=list,
    )
    
class PostersAndStickersPageResponse(BaseModel):
    grouped_by_base_category: list[GroupedByBaseCategory] = Field(
        default_factory=list,
    )