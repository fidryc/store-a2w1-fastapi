from pydantic import BaseModel
from typing import Optional


class SizeSchema(BaseModel):
    title: str
    base_category_id: Optional[int]


class MaterialSchema(BaseModel):
    title: str


class ColorSchema(BaseModel):
    title: str
    hex_code: Optional[str]


class BaseCategorySchema(BaseModel):
    title: str
    slug: str


class SubCategorySchema(BaseModel):
    base_category_id: int
    title: str
    slug: str


class ProductSchema(BaseModel):
    title: str
    description: Optional[str]
    base_price: float
    base_category_id: Optional[int]
    sub_category_id: Optional[int]
    material_id: Optional[int]
    simple_quantity: int


class ProductVariantSchema(BaseModel):
    product_id: int
    size_id: Optional[int]
    color_id: Optional[int]
    price_modifier: float
    quantity: int


class CollectionSchema(BaseModel):
    title: str
    description: Optional[str]


class CollectionProductSchema(BaseModel):
    collection_id: int
    product_id: int


class ProductPhotoSchema(BaseModel):
    product_id: int
    file_path: str
    is_primary: bool
    sort_order: int
