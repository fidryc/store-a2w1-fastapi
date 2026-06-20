from fastapi.responses import FileResponse

from app.core.logger import logger
from fastapi import Depends, HTTPException, UploadFile, APIRouter
from app.api.v1.dependency.uow import UOWDep

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
    
    try:
        photo_service = PhotoService(uow)
        id = (await photo_service.add(await file.read(), path))
        await uow.commit()
        return id
    except PhotoServiceException as e:
        raise HTTPException(status_code=e.status_code, detail=e.args[0])
    except Exception as e:
        logger.critical("Unknow error in delete-file", exc_info=True, extra={"path": path})
        raise HTTPException(status_code=e.status_code, detail=e.args[0])

@router.delete(
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
        raise HTTPException(status_code=500, detail=e.args[0])
    
    
HOME_ASSETS = {
    # логотип
    "logo": "/static/images/logo.png",

    # about секция
    "about_image": "/static/images/about-image.jpg",

    # carousel (блок "A2W1 КАК СМЫСЛ")
    "carousel_1": "/static/images/image-1.jpg",
    "carousel_2": "/static/images/image-2.jpg",
    "carousel_3": "/static/images/image-3.jpg",

    # collage (капсульные коллекции)
    "capsule_left_top": "/static/images/left-top.jpg",
    "capsule_left_bottom": "/static/images/left-bottom.jpg",

    "capsule_right_top": "/static/images/right-top.jpg",
    "capsule_right_bottom_large": "/static/images/right-bottom-long.jpg",
    "capsule_right_bottom_small_top": "/static/images/right-bottom-small-top.jpg",
    "capsule_right_bottom_small_bottom": "/static/images/right-bottom-small-bottom.jpg",

    # posters / stickers блок
    "posters_left": "/static/images/sticker-posters-left.jpg",
    "posters_middle_top": "/static/images/sticker-posters-middle-top.jpg",
    "posters_middle_bottom": "/static/images/sticker-posters-middle-bottom.jpg",
    "posters_right_top": "/static/images/sticker-posters-right-top.jpg",
    "posters_right_bottom": "/static/images/sticker-posters-right-bottom.jpg",

    # footer / misc (если нужно потом)
    "footer_vector": "/static/images/Vector 1.png"
}
@router.get("/api/assets")
def get_assets():
    return HOME_ASSETS

from fastapi import UploadFile, File, HTTPException
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "../../../"))

@router.post("/admin/assets/{key}/replace")
def replace_asset(key: str, file: UploadFile = File(...)):
    if key not in HOME_ASSETS:
        raise HTTPException(status_code=404, detail="Asset not found")

    # текущий путь
    old_path = HOME_ASSETS[key]
    real_path = os.path.join(PROJECT_ROOT, old_path.lstrip("/"))

    # проверка типа
    if file.content_type not in ["image/jpeg", "image/png", "image/webp"]:
        raise HTTPException(status_code=400, detail="Invalid file type")

    # удаляем старый файл
    if os.path.exists(real_path):
        os.remove(real_path)

    # сохраняем НОВЫЙ ФАЙЛ ПО ТОМУ ЖЕ ПУТИ
    with open(real_path, "wb") as buffer:
        buffer.write(file.file.read())

    return {
        "message": "replaced",
        "path": old_path
    }
    

@router.get("/admin/assets/{key}")
def get_asset(key: str):
    if key not in HOME_ASSETS:
        raise HTTPException(status_code=404, detail="Asset not found")

    old_path = HOME_ASSETS[key]
    real_path = os.path.join(PROJECT_ROOT, old_path.lstrip("/"))

    if not os.path.exists(real_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(real_path)