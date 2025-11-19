from typing import Generic, TypeVar, Type
from pydantic import BaseModel

from app.schemas.dto import (
    SizeDTO,
    MaterialDTO,
    ColorDTO,
    BaseCategoryDTO,
    SubCategoryDTO,
    ProductDTO,
    ProductVariantDTO,
    CollectionDTO,
    CollectionProductDTO,
    ProductPhotoDTO,
)


DTO = TypeVar("dto", bound=BaseModel)

class Mixin(Generic[DTO]):
    dto: Type[DTO]
    
    @classmethod
    def serialize_to_dto(cls, obj, *, from_attributes: bool=True) -> DTO:
        return cls.dto.model_validate(obj, from_attributes=from_attributes)
    

class SizeMixin(Mixin[SizeDTO]):
    dto = SizeDTO


class MaterialMixin(Mixin[MaterialDTO]):
    dto = MaterialDTO


class ColorMixin(Mixin[ColorDTO]):
    dto = ColorDTO


class BaseCategoryMixin(Mixin[BaseCategoryDTO]):
    dto = BaseCategoryDTO


class SubCategoryMixin(Mixin[SubCategoryDTO]):
    dto = SubCategoryDTO


class ProductMixin(Mixin[ProductDTO]):
    dto = ProductDTO


class ProductVariantMixin(Mixin[ProductVariantDTO]):
    dto = ProductVariantDTO


class CollectionMixin(Mixin[CollectionDTO]):
    dto = CollectionDTO


class CollectionProductMixin(Mixin[CollectionProductDTO]):
    dto = CollectionProductDTO


class ProductPhotoMixin(Mixin[ProductPhotoDTO]):
    dto = ProductPhotoDTO

    