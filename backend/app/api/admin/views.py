from sqladmin import ModelView
from app.db.models.models import (
    CollectionCategory, Photo, Size, Material, Color, BaseCategory, SubCategory,
    Product, ProductVariant, Collection, ProductPhoto, User
)


class SizeAdmin(ModelView, model=Size):
    column_list = [Size.id, Size.title, Size.base_category_id]
    column_searchable_list = [Size.title]
    column_sortable_list = [Size.id, Size.title]


class MaterialAdmin(ModelView, model=Material):
    column_list = [Material.id, Material.title]
    column_searchable_list = [Material.title]
    column_sortable_list = [Material.id, Material.title]


class ColorAdmin(ModelView, model=Color):
    column_list = [Color.id, Color.title, Color.hex_code]
    column_searchable_list = [Color.title]
    column_sortable_list = [Color.id, Color.title]


class BaseCategoryAdmin(ModelView, model=BaseCategory):
    column_list = [BaseCategory.id, BaseCategory.title, BaseCategory.slug]
    column_searchable_list = [BaseCategory.title, BaseCategory.slug]
    column_sortable_list = [BaseCategory.id, BaseCategory.title]


class SubCategoryAdmin(ModelView, model=SubCategory):
    column_list = [
        SubCategory.id, SubCategory.title,
        SubCategory.slug, SubCategory.base_category_id
    ]
    column_searchable_list = [SubCategory.title, SubCategory.slug]
    column_sortable_list = [SubCategory.id, SubCategory.title]


class ProductAdmin(ModelView, model=Product):
    column_list = [
        Product.id, Product.title, Product.base_price,
        Product.base_category_id, Product.sub_category_id,
        Product.material_id, Product.simple_quantity
    ]
    column_searchable_list = [Product.title]
    column_sortable_list = [Product.id, Product.title, Product.base_price]


class ProductVariantAdmin(ModelView, model=ProductVariant):
    column_list = [
        ProductVariant.id,
        ProductVariant.product_id,
        ProductVariant.size_id,
        ProductVariant.color_id,
        ProductVariant.price_modifier,
        ProductVariant.quantity
    ]
    # column_sortable_list = [
    #     ProductVariant.id,
    #     ProductVariant.price_modifier,
    #     ProductVariant.quantity
    # ]


class CollectionAdmin(ModelView, model=Collection):
    column_list = [Collection.id, Collection.title]
    column_searchable_list = [Collection.title]
    column_sortable_list = [Collection.id, Collection.title]


# class CollectionProductAdmin(ModelView, model=CollectionProduct):
#     column_list = [
#         CollectionProduct.id,
#         CollectionProduct.collection_id,
#         CollectionProduct.product_id
#     ]
#     column_sortable_list = [CollectionProduct.id]


class ProductPhotoAdmin(ModelView, model=ProductPhoto):
    column_list = [
        ProductPhoto.id,
        ProductPhoto.product_id,
        ProductPhoto.photo_id,
        ProductPhoto.is_primary,
        ProductPhoto.sort_order
    ]
    column_sortable_list = [ProductPhoto.id, ProductPhoto.sort_order]
    
class PhotoAdmin(ModelView, model=Photo):
    column_list = [
        Photo.id,
        Photo.file_path,
    ]
    column_sortable_list = [Photo.id, Photo.file_path]
    
    can_delete = False
    can_edit = False
    can_create = False
    

class UserAdmin(ModelView, model=User):
    column_list = [c for c in User.__table__.columns]
    

class CollecctionCategoryAdmin(ModelView, model=CollectionCategory):
    column_list = [c for c in CollectionCategory.__table__.columns]