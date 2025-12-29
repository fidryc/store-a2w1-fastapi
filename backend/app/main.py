import datetime
from fastapi import FastAPI, Response, Request
from fastapi.staticfiles import StaticFiles
from starlette.middleware import Middleware
from sqladmin import Admin

from app.db.session import engine
from app.api.admin.views import (
    CollecctionCategoryAdmin, PhotoAdmin, SizeAdmin, MaterialAdmin, ColorAdmin, BaseCategoryAdmin, SubCategoryAdmin,
    ProductAdmin, ProductVariantAdmin, CollectionAdmin, ProductPhotoAdmin, UserAdmin
)
from app.repositories.implementations.sqlalchemy.base_uow import BaseUOW
from app.services.implementations.collection_service import CollectionService
from app.services.implementations.product_service import ProductService


from app.api.v1.dependency.user import CurrentUserDep

from app.api.v1.routers.images import router as images_router
from app.api.v1.routers.users import router as users_router
from app.api.v1.routers.frontend import router as frontend_router
from app.api.v1.routers.test import router as test_router
from app.core.logger import logger

from fastapi.openapi.docs import get_swagger_ui_html

from app.api.v1.middlewares.check_admin import IsAdminMiddleware
from app.utils.add_admin_views import add_views

app = FastAPI(
    docs_url=None,
    redoc_url=None,
    openapi_url="/openapi.json"
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Подключение роутеров
app.include_router(frontend_router) 
app.include_router(images_router)
app.include_router(users_router)
app.include_router(test_router)

admin = Admin(app, engine, middlewares=[Middleware(IsAdminMiddleware),])

# Заменить на функцию добавление наследников из файла ModelView

add_views(admin.add_view)

@app.get("/docs", include_in_schema=False)
async def custom_docs(user: CurrentUserDep, response: Response):
    if user.role != "admin":
        from fastapi.responses import HTMLResponse

        return HTMLResponse(
            content="<h1>403 Нет доступа</h1>",
            status_code=403
        )
    else:
        html = get_swagger_ui_html(openapi_url="/openapi.json", title="Docs")
        for k, v in html.headers.items():
            response.headers[k] = v

            response.status_code = html.status_code
            response.body = html.body

        return response