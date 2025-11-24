from venv import logger
from fastapi import Depends, HTTPException, UploadFile, APIRouter
from sqlalchemy import delete
from app.api.v1.dependency.uow import UOWDep
import aiofiles

from app.api.v1.dependency.user import AdminDep, get_admin
from app.services.exceptions.photo import PhotoServiceException
from app.services.implementations.photo_service import PhotoService

router = APIRouter(
    prefix="/api/v1/images",
    tags=["Работа с файлами"]
)

@router.post(
    "/upload-file",
    dependencies=[Depends(get_admin)]
)
async def upload_file(path: str, uow: UOWDep, file: UploadFile):
    # проверка прав. Проверка уникальности path. Сжатие. 
    
    try:
        photo_service = PhotoService(uow)
        return (await photo_service.add(await file.read(), path))
    except PhotoServiceException as e:
        raise HTTPException(status_code=e.status_code, detail=e.args[0])
    except Exception as e:
        logger.critical("Unknow error in delete-file", exc_info=True, extra={"path": path})
        raise HTTPException(status_code=e.status_code, detail=e.args[0])

@router.get(
    "/delete-file",
    dependencies=[Depends(get_admin)]
)
async def delete_file(path: str, uow: UOWDep):
    # проверка прав. Проверка уникальности path. Сжатие. 
    try:
        photo_service = PhotoService(uow)
        return (await photo_service.delete(path))
    except PhotoServiceException as e:
        raise HTTPException(status_code=e.status_code, detail=e.args[0])
    except Exception as e:
        logger.critical("Unknow error in delete-file", exc_info=True, extra={"path": path})
        raise HTTPException(status_code=e.status_code, detail=e.args[0])
    
@router.get("/admin-stuff")
async def admin_route(user: AdminDep):
    return {"ok": True}