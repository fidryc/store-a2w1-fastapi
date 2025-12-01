from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.repositories.implementations.sqlalchemy.base_uow import BaseUOW
from app.services.implementations.collection_service import CollectionService
from app.services.implementations.product_service import ProductService

from app.api.v1.dependency.uow import UOWDep
from app.services.implementations.frontend_service import FrontendBaseService
from app.services.exceptions.collection import CollectionServiceException

router = APIRouter(tags=["Frontend"])


templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse, name="home")
async def home(request: Request, uow: UOWDep):
    """Главная страница"""
    try:
        fr_sv = FrontendBaseService(uow, CollectionService(uow, ProductService(uow)))
        data = await fr_sv.base_data()
        print(data)
        # Подготовка контекста для шаблона
        context = {
            "request": request,
            "large_collections": data.get('large_collection'),  # (category, [collections])
            "capsule_collections": data.get('capsule'),  # (category, [collections])
        }
        
        return templates.TemplateResponse(
            request=request, 
            name="base.html", 
            context=context
        )
    except (CollectionServiceException) as e:
        raise HTTPException(e.status_code, e.args[0])