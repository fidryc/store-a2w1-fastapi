from fastapi import FastAPI
from sqladmin import Admin

from app.db.session import engine, session_maker
from app.api.admin.views import (
    SizeAdmin, MaterialAdmin, ColorAdmin, BaseCategoryAdmin, SubCategoryAdmin,
    ProductAdmin, ProductVariantAdmin, CollectionAdmin, CollectionProductAdmin, ProductPhotoAdmin
)
from app.schemas.dto import SizeDTO
from app.schemas.schemas import SizeSchema
from app.repositories.implementations.sqlalchemy.base_uow import BaseUOW

app = FastAPI()

admin = Admin(app, engine)

admin.add_view(SizeAdmin)
admin.add_view(MaterialAdmin)
admin.add_view(ColorAdmin)
admin.add_view(BaseCategoryAdmin)
admin.add_view(SubCategoryAdmin)
admin.add_view(ProductAdmin)
admin.add_view(ProductVariantAdmin)
admin.add_view(CollectionAdmin)
admin.add_view(CollectionProductAdmin)
admin.add_view(ProductPhotoAdmin)