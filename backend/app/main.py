import datetime
from fastapi import FastAPI, Response, Request
from starlette.middleware import Middleware
from sqladmin import Admin

from app.db.session import engine
from app.api.admin.views import (
    CollecctionCategoryAdmin, PhotoAdmin, SizeAdmin, MaterialAdmin, ColorAdmin, BaseCategoryAdmin, SubCategoryAdmin,
    ProductAdmin, ProductVariantAdmin, CollectionAdmin, CollectionProductAdmin, ProductPhotoAdmin, UserAdmin
)
from app.repositories.implementations.sqlalchemy.base_uow import BaseUOW
from app.services.implementations.collection_service import CollectionService
from app.services.implementations.product_service import ProductService


from app.api.v1.dependency.user import CurrentUserDep

from app.api.v1.routers.images import router as images_router
from app.api.v1.routers.users import router as users_router
from app.core.logger import logger

from fastapi.openapi.docs import get_swagger_ui_html

from app.api.v1.middlewares.check_admin import IsAdminMiddleware

app = FastAPI(
    docs_url=None,
    redoc_url=None,
    openapi_url="/openapi.json"
)
 
app.include_router(images_router)
app.include_router(users_router)

admin = Admin(app, engine, middlewares=[Middleware(IsAdminMiddleware),])

# Заменить на функцию добавление наследников из файла ModelView
admin.add_view(SizeAdmin)
admin.add_view(MaterialAdmin)
admin.add_view(ColorAdmin)
admin.add_view(BaseCategoryAdmin)
admin.add_view(SubCategoryAdmin)
admin.add_view(ProductAdmin)
admin.add_view(ProductVariantAdmin)
admin.add_view(CollecctionCategoryAdmin)
admin.add_view(CollectionAdmin)
admin.add_view(CollectionProductAdmin)
admin.add_view(ProductPhotoAdmin)
admin.add_view(UserAdmin)
admin.add_view(PhotoAdmin)

@app.get("/test")
async def test():
    async with BaseUOW() as uow:
        pr_service = ProductService(uow)
        cl_service = CollectionService(uow, product_service=pr_service)
        print(await cl_service.categories_with_cats())
    
@app.middleware("http")
async def check_time(request: Request, call_next):
    start = datetime.datetime.now()
    response = await call_next(request)
    time_request = (datetime.datetime.now() - start).total_seconds()
    logger.debug("Time for request", extra={"sectonds": time_request})
    return response

# Проверка admin роли у пользователя перед тем как отдавать swagger
@app.get("/docs", include_in_schema=False)
async def custom_docs(user: CurrentUserDep):
    if user.role != "admin":
        from fastapi.responses import HTMLResponse

        return HTMLResponse(
            content="<h1>403 Нет доступа</h1>",
            status_code=403
        )
    else:
        return get_swagger_ui_html(
            openapi_url="/openapi.json",
            title="Docs"
        )
        