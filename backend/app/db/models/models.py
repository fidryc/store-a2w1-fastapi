from sqlalchemy import String, Integer, ForeignKey, Numeric, Boolean, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.orm import relationship
from typing import Optional
from app.db.mixins.mixins import BaseCategoryMixin, CollectionCategoryMixin, CollectionMixin, CollectionProductLimitMixin, Mixin, PhotoMixin, ProductMixin, ProductPhotoMixin, ProductVariantMixin, SizeMixin, MaterialMixin, ColorMixin, SubCategoryMixin, UserMixin


class Base(Mixin, DeclarativeBase):
    pass


class Size(SizeMixin, Base):
    __tablename__ = "sizes"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(64), index=True)
    base_category_id: Mapped[Optional[int]] = mapped_column(ForeignKey("base_categories.id"), index=True)

    base_category = relationship("BaseCategory", back_populates="size")
    
    def __str__(self):
        return f"Size: {self.title}"
    
    
class Material(MaterialMixin, Base):
    __tablename__ = "materials"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(128))

    def __str__(self):
        return f"Material: {self.title}"


class Color(ColorMixin, Base):
    __tablename__ = "colors"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(32), index=True)
    hex_code: Mapped[Optional[str]] = mapped_column(String(7))

    def __str__(self):
        return f"Color: {self.title}"


class BaseCategory(BaseCategoryMixin, Base):
    __tablename__ = "base_categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(64))
    slug: Mapped[str] = mapped_column(String(64))

    size = relationship("Size", back_populates="base_category")
    sub_category = relationship("SubCategory", back_populates="base_category")
    
    def __str__(self):
        return f"Base Category: {self.title}"


class SubCategory(SubCategoryMixin, Base):
    __tablename__ = "sub_categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    base_category_id: Mapped[int] = mapped_column(ForeignKey("base_categories.id"), index=True)
    title: Mapped[str] = mapped_column(String(64))
    slug: Mapped[str] = mapped_column(String(64))

    base_category = relationship("BaseCategory", back_populates="sub_category")
    
    def __str__(self):
        return f"Sub Category: {self.title}"


class Product(ProductMixin, Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(Text)
    base_price: Mapped[float] = mapped_column(Numeric(10, 2))
    base_category_id: Mapped[Optional[int]] = mapped_column(ForeignKey("base_categories.id"), index=True)
    sub_category_id: Mapped[Optional[int]] = mapped_column(ForeignKey("sub_categories.id"), index=True)
    material_id: Mapped[Optional[int]] = mapped_column(ForeignKey("materials.id"), index=True)
    collection_id: Mapped[Optional[int]] = mapped_column(ForeignKey("collections.id"), index=True, nullable=True)
    simple_quantity: Mapped[int] = mapped_column(Integer)
    
    material = relationship("Material")
    base_category = relationship("BaseCategory")
    sub_category = relationship("SubCategory")
    collection = relationship("Collection")
    photos = relationship("ProductPhoto")
    
    def __str__(self):
        return f"Product: {self.title}"


class ProductVariant(ProductVariantMixin, Base):
    __tablename__ = "product_variants"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), index=True)
    size_id: Mapped[Optional[int]] = mapped_column(ForeignKey("sizes.id"), index=True)
    color_id: Mapped[Optional[int]] = mapped_column(ForeignKey("colors.id"), index=True)
    price_modifier: Mapped[float] = mapped_column(Numeric(10, 2), default=0)
    quantity: Mapped[int] = mapped_column(Integer, default=0)

    product = relationship("Product")
    size = relationship("Size", lazy="select")
    color = relationship("Color")
    
    def __str__(self):
        return f"Product variant #{self.id}"


class CollectionCategory(CollectionCategoryMixin, Base):
    __tablename__ = "collection_categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(32))
    slug: Mapped[str] = mapped_column(String(32), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    
    def __str__(self):
        return f"Collection category: {self.title}"
    
    
class Collection(CollectionMixin, Base):
    __tablename__ = "collections"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(Text)
    photo_id: Mapped[int] = mapped_column(ForeignKey("photos.id"), index=True)
    collection_category_id: Mapped[int] = mapped_column(ForeignKey("collection_categories.id"), index=True)
    
    photo = relationship("Photo")
    collection_category = relationship("CollectionCategory")
    
    def __str__(self):
        return f"Collection: {self.title}"


class CollectionProductLimit(CollectionProductLimitMixin, Base):
    """Модель для определения количества на товары в определенной коллекци и категории"""
    __tablename__ = "collection_product_limits"

    id: Mapped[int] = mapped_column(primary_key=True)
    collection_id: Mapped[int] = mapped_column(ForeignKey("collections.id"), index=True)
    base_category_id: Mapped[int] = mapped_column(ForeignKey("base_categories.id"), index=True)
    quantity: Mapped[int] = mapped_column(Integer)
    
    collection = relationship("Collection")
    base_category = relationship("BaseCategory")

    
class ProductPhoto(ProductPhotoMixin, Base):
    __tablename__ = "product_photos"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), index=True)
    photo_id: Mapped[int] = mapped_column(ForeignKey("photos.id"), index=True)
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    
    product = relationship("Product")
    photo = relationship("Photo", lazy="selectin")
    
    
class Photo(PhotoMixin, Base):
    __tablename__ = "photos"

    def __str__(self):
        return f"{self.file_path}"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    file_path: Mapped[str] = mapped_column(String(500), unique=True)
    

class User(UserMixin, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(256), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(256), nullable=False)
    role: Mapped[str] = mapped_column(String(32), nullable=True)
    

