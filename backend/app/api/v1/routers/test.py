from sys import exc_info
from venv import logger
from fastapi import Depends, HTTPException, Request, UploadFile, APIRouter
from app.api.v1.dependency.uow import UOWDep

from app.api.v1.dependency.user import AdminDep, get_admin, get_auth_tokens
from app.services.exceptions.photo import PhotoServiceException
from app.services.implementations.photo_service import PhotoService
from app.services.implementations.collection_service import CollectionService
from app.services.implementations.product_service import ProductService
from app.services.exceptions.collection import CollectionServiceException

router = APIRouter(
    prefix="/api/v1/test_all_services",
    tags=["Тестирование всех сервисов"]
)

@router.get(
    "/test",
    # dependencies=[Depends(get_admin)]
)
async def test(request: Request, uow: UOWDep):
    print(request.cookies.get("refresh_token", None))
    input()
    
    cl_s = CollectionService(uow, ProductService(uow))
    try:
        print(await cl_s.all_collections_with_photo())
        print()
        print(await cl_s.all_collections_with_products())
        print()
        print(await cl_s.categories_with_collections())
        print()
        print(await cl_s.get_collection_by_id(4))
        print()
        print(await cl_s.get_products_by_collection_id(4))
    except CollectionServiceException as e:
        raise HTTPException(status_code=e.status_code, detail=e.args[0])
    except Exception as e:
        logger.critical("Unknow error in delete-file", exc_info=True)
        raise HTTPException(status_code=500)
    
