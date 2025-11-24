from re import S
from typing import Optional
from pydantic import BaseModel


class SizeDTO(BaseModel):
    id: int
    title: str
    base_category_id: Optional[int] = None


class MaterialDTO(BaseModel):
    id: int
    title: str


class ColorDTO(BaseModel):
    id: int
    title: str
    hex_code: Optional[str]


class BaseCategoryDTO(BaseModel):
    id: int
    title: str
    slug: str


class SubCategoryDTO(BaseModel):
    id: int
    base_category_id: int
    title: str
    slug: str


class ProductDTO(BaseModel):
    id: int
    title: str
    description: Optional[str]
    base_price: float
    base_category_id: Optional[int]
    sub_category_id: Optional[int]
    material_id: Optional[int]
    simple_quantity: int


class ProductVariantDTO(BaseModel):
    id: int
    product_id: int
    size_id: Optional[int]
    color_id: Optional[int]
    price_modifier: float
    quantity: int


class PhotoDTO(BaseModel):
    id: int
    file_path: str
    
    
class CollectionCategoryDTO(BaseModel):
    id: int
    title: str
    description: str
    sort_order: int

class CollectionDTO(BaseModel):
    id: int
    title: str
    description: Optional[str]
    photo: PhotoDTO
    collection_category: CollectionCategoryDTO


class CollectionProductDTO(BaseModel):
    id: int
    collection_id: int
    product_id: int


class ProductPhotoDTO(BaseModel):
    id: int
    product_id: int
    file_path: str
    is_primary: bool
    sort_order: int
    
    
class UserDTO(BaseModel):
    id: int
    email: str
    hashed_password: str
    role: str | None
