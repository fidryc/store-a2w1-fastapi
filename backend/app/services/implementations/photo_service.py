from fastapi import status
import aiofiles

from app.repositories.exceptions.base_exc import RepositoryExc
from app.repositories.interfaces.abc_base_uow import IBaseUOW
from app.services.exceptions.photo import PhotoServiceException

import os
from app.core.logger import logger
from app.constants.files import Paths

class PhotoService:
    def __init__(self, uow: IBaseUOW, file_optimizer = None):
        self.uow = uow
        # self.file_optimizer = file_optimizer
        
    @staticmethod
    def __validate_file_name(file_path: str):
        if not isinstance(file_path, str):
            raise PhotoServiceException(
                "Имя файла должно быть строкой",
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT
            )
        if any(symbol in file_path for symbol in ("/", "\\", ".")):
            raise PhotoServiceException(
                "Имя имеет неверный формат. Уберите символы '\' или '/' или '.'",
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT
            )
    
    async def add(self, file: bytes, file_path: str) -> int:
        """
        Создание файла на сервере.
        Добавление к товару фотки происходит через админ панель
        """
        
        self.__validate_file_name(file_path=file_path)
        if len(await self.uow.photo_repo.get_by_filters(file_path=file_path)) != 0:
            raise PhotoServiceException(
                "Файл с таким именем уже существует. Выбирите другое имя либо удалите фотку с таким именем",
                status_code=status.HTTP_409_CONFLICT
            )
        try:
            id = await self.uow.photo_repo.add({"file_path": file_path})
        except RepositoryExc as e:
            raise PhotoServiceException(
                "Ошибка добавления фото",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            ) from e
            
        # try:
        #     optimize_file = self.file_optimizer.optimize_file()
        # except FileOptimizerException as e:
        #     logger.warning(
        #         "Failed optimize file",
        #         exc_info=True,
        #         extra={"file": file}
        #     )
        # if optimize_file:
        #     file = optimize_file
        try:
            async with aiofiles.open(f"{Paths.UPLOADS_DIR}/{file_path}.jpg", "wb") as f:
                await f.write(file)
        except Exception as e:
            logger.critical(msg="Failed write file", exc_info=True, extra={"file": file})
            await self.uow.photo_repo.delete_by_filters(id=id)
            raise PhotoServiceException("Не получилось записать файл", status_code=500)
        return id
    
    
    async def delete(self, file_path: str) -> list[int]:
        """Удаление фотки с сервера и из базы"""
        self.__validate_file_name(file_path)
        path = f"{Paths.UPLOADS_DIR}/{file_path}.jpg"
        if not os.path.exists(path):
            raise PhotoServiceException(
                "Такого файла не существует",
                status_code=status.HTTP_404_NOT_FOUND
            )
        try:
            ids = await self.uow.photo_repo.delete_by_filters(file_path=file_path)
        except RepositoryExc as e:
            raise PhotoServiceException(
                "Ошибка удаления. Скорее всего у продуктов есть ссылка на эту фотку. Удалите сначала фотографию у продуктов",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            ) from e
        try:
            os.remove(path=path)
        except Exception as e:
            logger.critical(
                "Failed to delete photo",
                extra={"file_path": path},
                exc_info=True
            )
            raise PhotoServiceException(
                "Ошибка удаления файла",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            ) from e
        
        return ids