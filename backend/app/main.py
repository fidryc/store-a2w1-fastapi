import datetime
from fastapi import FastAPI, Response, Request
from fastapi.staticfiles import StaticFiles
from starlette.middleware import Middleware
from sqladmin import Admin

from app.db.session import engine

from app.api.v1.dependency.user import CurrentUserDep

from app.api.v1.routers.images import router as images_router
from app.api.v1.routers.users import router as users_router
from app.frontend import router as frontend_router

from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse

from app.api.v1.middlewares.check_admin import IsAdminMiddleware
from app.utils.add_admin_views import add_views

app = FastAPI(
    docs_url=None,
    redoc_url=None,
    openapi_url="/openapi.json"
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(frontend_router) 
app.include_router(images_router)
app.include_router(users_router)

admin = Admin(app, engine, middlewares=[Middleware(IsAdminMiddleware),])

add_views(admin.add_view)

@app.get("/docs", include_in_schema=False)
async def custom_docs(user: CurrentUserDep, response: Response):
    if user.role != "admin":
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