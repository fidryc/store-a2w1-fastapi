from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.services.implementations.collection_service import CollectionService

from app.api.v1.dependency.uow import UOWDep
from app.services.exceptions.collection import CollectionServiceException
from app.api.v1.dependency.application import BasePageServiceDep
from app.application.services.collections_page import CollectionsPageService
from app.services.implementations.product_service import ProductService
from app.services.exceptions.product import ProductServiceException

router = APIRouter(tags=["Frontend"])


templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse, name="home")
async def home(request: Request, base_page_service: BasePageServiceDep):
    """Главная страница"""
    try:
        base_page_data = await base_page_service.get_home_page_data()
        return templates.TemplateResponse(
            request=request, 
            name="home.html", 
            context={"request": request, "base_page_data": base_page_data}
        )
    except (CollectionServiceException) as e:
        raise HTTPException(e.status_code, e.args[0])

  
@router.get("/all", response_class=HTMLResponse, name="home")
async def all_products(request: Request, base_page_service: BasePageServiceDep, uow: UOWDep):
    """Главная страница"""
    try:
        collection_service=CollectionService(uow=uow)
        product_service=ProductService(uow=uow, collection_service=collection_service)
        base_page_data = await base_page_service.get_home_page_data()
        return templates.TemplateResponse(
            request=request, 
            name="all_products.html", 
            context={
                "request": request,
                "base_page_data": base_page_data,
                "products": await product_service.all_products()
                
                }
        )
    except (CollectionServiceException, ProductServiceException) as e:
        raise HTTPException(e.status_code, e.args[0])


@router.get(
    "/collections/collection_category_id/{collection_category_id}",
    response_class=HTMLResponse,
    name="collections_by_cat_id"
)
async def collections_by_cat_id(
    request: Request,
    uow: UOWDep,
    base_page_service: BasePageServiceDep,
    collection_category_id: int
):
    """Страница коллекций по id категории"""
    try:
        collection_service=CollectionService(uow=uow)
        collection_page_service = CollectionsPageService(
            collection_service=collection_service,
            product_service=ProductService(uow=uow, collection_service=collection_service)
        )
        return templates.TemplateResponse(
            request=request, 
            name="collections_by_cat_id.html", 
            context={
                "request": request,
                "base_page_data": await base_page_service.get_home_page_data(),
                "collection_page_data": await collection_page_service.get_collections_by_cat_id_page_data(
                    collection_category_id=collection_category_id
                )
            }
        )
    except (CollectionServiceException, ProductServiceException) as e:
        raise HTTPException(e.status_code, e.args[0])
    
@router.get(
    "/collection/{collection_id}",
    response_class=HTMLResponse,
    name="collection_by_id"
)
async def collections_by_id(
    request: Request,
    uow: UOWDep,
    base_page_service: BasePageServiceDep,
    collection_id: int
):
    """Получение страницы с товаром коллекции"""
    try:
        collection_service=CollectionService(uow=uow)
        collection_page_service = CollectionsPageService(
            collection_service=collection_service,
            product_service=ProductService(uow=uow, collection_service=collection_service)
        )
        return templates.TemplateResponse(
            request=request, 
            name="collection_by_id.html", 
            context={
                "request": request,
                "base_page_data": await base_page_service.get_home_page_data(),
                "collection_page_data": await collection_page_service.get_collection_by_id_page_data(collection_id=collection_id)
            }
        )
    except (CollectionServiceException, ProductServiceException) as e:
        raise HTTPException(e.status_code, e.args[0])
    

@router.get(
    "/posters_stickers",
    response_class=HTMLResponse,
    name="posters_stickers"
)
async def posters_stickers(
    request: Request,
    uow: UOWDep,
    base_page_service: BasePageServiceDep
):
    """Получение страницы постеров и стикеров"""
    try:
        collection_service=CollectionService(uow=uow)
        collection_page_service = CollectionsPageService(
            collection_service=collection_service,
            product_service=ProductService(uow=uow, collection_service=collection_service)
        )
        return templates.TemplateResponse(
            request=request, 
            name="collection_by_id.html", 
            context={
                "request": request,
                "base_page_data": await base_page_service.get_home_page_data(),
                "posters_stickers_data": await collection_page_service.get_posters_and_stickers_page_data()
            }
        )
    except (CollectionServiceException, ProductServiceException) as e:
        raise HTTPException(e.status_code, e.args[0])
    
    
@router.get(
    "/product/{product_id}",
    response_class=HTMLResponse,
    name="product_by_id"
)
async def product_by_id(
    request: Request,
    uow: UOWDep,
    base_page_service: BasePageServiceDep,
    product_id: int
):
    """Получение страницы с товаром коллекции"""
    product_service = ProductService(uow=uow, collection_service=CollectionService(uow))
    try:
        product = await product_service.product_with_details(id=product_id)
        return templates.TemplateResponse(
                request=request, 
                name="product.html", 
                context={
                    "request": request,
                    "base_page_data": await base_page_service.get_home_page_data(),
                    "product": product,
                }
            )
    except (ProductServiceException, ProductServiceException) as e:
        raise HTTPException(e.status_code, e.args[0])
        
        
@router.get("/admin-login", response_class=HTMLResponse)
async def admin_login_page(request: Request):
    return templates.TemplateResponse("admin_login.html", {"request": request})