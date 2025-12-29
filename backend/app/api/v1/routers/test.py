from app.core.logger import logger
from fastapi import HTTPException, Request, APIRouter
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

    
