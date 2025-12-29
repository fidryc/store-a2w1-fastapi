from sqladmin import ModelView
from app.db.models.models import (
    CollectionCategory, Photo, Size, Material, Color, BaseCategory, SubCategory,
    Product, ProductVariant, Collection, ProductPhoto, User
)
from markupsafe import Markup


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
    # скрывает relationship из формы создания/редактирования
    form_excluded_columns = ["photos"]

    # скрывает relationship со страницы деталей
    column_details_exclude_list = ["photos"]
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


class CollectionAdmin(ModelView, model=Collection):
    column_list = [Collection.id, Collection.title]
    column_searchable_list = [Collection.title]
    column_sortable_list = [Collection.id, Collection.title]


class ProductPhotoAdmin(ModelView, model=ProductPhoto):
    column_list = [
        ProductPhoto.id,
        ProductPhoto.product_id,
        ProductPhoto.photo_id,
        ProductPhoto.is_primary,
        ProductPhoto.sort_order,
        "photo_preview"
    ]
    column_sortable_list = [ProductPhoto.id, ProductPhoto.sort_order]
    
    @staticmethod
    def photo_preview(obj, _):
        if not obj.photo:
            return "—"

        return Markup(
            f"""
            <img 
                src="/static/uploads/{obj.photo.file_path}.jpg"
                style="
                    height: 120px;
                    border-radius: 8px;
                    object-fit: cover;
                "
            />
            """
        )

    column_formatters = {
        "photo_preview": photo_preview
    }

    column_labels = {
        "photo_preview": "Фото"
    }
    
class PhotoAdmin(ModelView, model=Photo):
    column_list = [
        Photo.id,
        Photo.file_path,
        "preview"
    ]
    column_sortable_list = [Photo.id, Photo.file_path]
    
    can_delete = False
    can_edit = False
    can_create = False
    
    def preview(self, obj):
        return Markup(
            f'<img src="/static/uploads/{obj.file_path}.jpg" height="700">'
        )

    column_formatters = {
        "preview": lambda obj, _: PhotoAdmin.preview(None, obj)
    }
    

class UserAdmin(ModelView, model=User):
    column_list = [c for c in User.__table__.columns]
    

class CollecctionCategoryAdmin(ModelView, model=CollectionCategory):
    column_list = [c for c in CollectionCategory.__table__.columns]