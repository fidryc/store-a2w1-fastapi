from app.repositories.implementations.sqlalchemy.repo.base_category_repo import BaseCategoryRepository
from app.repositories.implementations.sqlalchemy.repo.collection_category import CollectionCategoryRepository
from app.repositories.implementations.sqlalchemy.repo.collection_repo import CollectionRepository
from app.repositories.implementations.sqlalchemy.repo.color_repo import ColorRepository
from app.repositories.implementations.sqlalchemy.repo.material_repo import MaterialRepository
from app.repositories.implementations.sqlalchemy.repo.photo_repo import PhotoRepository
from app.repositories.implementations.sqlalchemy.repo.product_repo import ProductRepository
from app.repositories.implementations.sqlalchemy.repo.product_variant_repo import ProductVariantRepository
from app.repositories.implementations.sqlalchemy.repo.size_repo import SizeRepository
from app.repositories.implementations.sqlalchemy.repo.sub_category_repo import SubCategoryRepository
from app.repositories.implementations.sqlalchemy.repo.product_photo_repo import ProductPhotoRepository
from app.repositories.interfaces.abc_base_uow import IBaseUOW

from app.db.session import session_maker

from sqlalchemy.ext.asyncio import AsyncSession
from app.core.logger import logger
from typing_extensions import Self

from app.repositories.implementations.sqlalchemy.repo.user_repo import UserRepository
from app.repositories.implementations.sqlalchemy.repo.collection_product_limit_repository import CollectionProductLimitRepository

class BaseUOW(IBaseUOW):
    def __init__(self):
        self.__size_repo: SizeRepository | None = None
        self.__material_repo: MaterialRepository | None = None
        self.__color_repo: ColorRepository | None = None
        self.__base_category_repo: BaseCategoryRepository | None = None
        self.__sub_category_repo: SubCategoryRepository | None = None
        self.__product_repo: ProductRepository | None = None
        self.__product_variant_repo: ProductVariantRepository | None = None
        self.__collection_repo: CollectionRepository | None = None
        self.__collection_product_limit_repo: CollectionProductLimitRepository | None = None
        self.__collection_category_repo: CollectionCategoryRepository | None = None
        self.__product_photo_repo: ProductPhotoRepository | None = None
        self.__photo_repo: PhotoRepository | None = None
        self.__user_repo: UserRepository | None = None
        
        self.__session_factory = session_maker
        self.__session: AsyncSession | None = None


    async def __aenter__(self) -> Self:
        if not self.__session:
            self.__session = self.__session_factory()
        return self
    
    async def __aexit__(self, exc_type, exc, tb):
        if exc_type:
            await self.rollback()
        await self.close()
    
    async def rollback(self) -> None:
        if self.__session:
            await self.__session.rollback()
            logger.debug(msg="UOW: Rollback session")
        else:
            logger.warning(msg="UOW Failed: cannot rollback session")
    
    async def commit(self) -> None:
        if self.__session:
            await self.__session.commit()
            logger.debug(msg="UOW: Commit session")
        else:
            logger.warning(msg="UOW Failed: cannot commit session")
    
    async def close(self) -> None:
        if self.__session:
            await self.__session.close()
            logger.debug(msg="UOW: close session")
        else:
            logger.warning(msg="UOW Failed: cannot close session, __session=None")
    
    @property
    def size_repo(self) -> SizeRepository:
        self.__validate_session()
        if not self.__size_repo:
            self.__size_repo = SizeRepository(self.__session)
        return self.__size_repo
    
    @property
    def base_category_repo(self) -> BaseCategoryRepository:
        self.__validate_session()
        if not self.__base_category_repo:
            self.__base_category_repo = BaseCategoryRepository(self.__session)
        return self.__base_category_repo

    @property
    def material_repo(self) -> MaterialRepository:
        self.__validate_session()
        if not self.__material_repo:
            self.__material_repo = MaterialRepository(self.__session)
        return self.__material_repo
    
    @property
    def color_repo(self) -> ColorRepository:
        self.__validate_session()
        if not self.__color_repo:
            self.__color_repo = ColorRepository(self.__session)
        return self.__color_repo

    @property
    def sub_category_repo(self) -> SubCategoryRepository:
        self.__validate_session()
        if not self.__sub_category_repo:
            self.__sub_category_repo = SubCategoryRepository(self.__session)
        return self.__sub_category_repo

    @property
    def product_repo(self) -> ProductRepository:
        self.__validate_session()
        if not self.__product_repo:
            self.__product_repo = ProductRepository(self.__session)
        return self.__product_repo

    @property
    def product_variant_repo(self) -> ProductVariantRepository:
        self.__validate_session()
        if not self.__product_variant_repo:
            self.__product_variant_repo = ProductVariantRepository(self.__session)
        return self.__product_variant_repo

    @property
    def collection_repo(self) -> CollectionRepository:
        self.__validate_session()
        if not self.__collection_repo:
            self.__collection_repo = CollectionRepository(self.__session)
        return self.__collection_repo
    
    @property
    def collection_product_limit_repo(self) -> CollectionProductLimitRepository:
        self.__validate_session()
        if not self.__collection_product_limit_repo:
            self.__collection_product_limit_repo = CollectionProductLimitRepository(self.__session)
        return self.__collection_product_limit_repo
    
    @property
    def collection_category_repo(self) -> CollectionCategoryRepository:
        self.__validate_session()
        if not self.__collection_category_repo:
            self.__collection_category_repo = CollectionCategoryRepository(self.__session)
        return self.__collection_category_repo


    @property
    def product_photo_repo(self) -> ProductPhotoRepository:
        self.__validate_session()
        if not self.__product_photo_repo:
            self.__product_photo_repo = ProductPhotoRepository(self.__session)
        return self.__product_photo_repo
    
    @property
    def photo_repo(self) -> PhotoRepository:
        self.__validate_session()
        if not self.__photo_repo:
            self.__photo_repo = PhotoRepository(self.__session)
        return self.__photo_repo
    
    @property
    def user_repo(self) -> UserRepository:
        self.__validate_session()
        if not self.__user_repo:
            self.__user_repo = UserRepository(self.__session)
        return self.__user_repo
    
    def __validate_session(self):
        if self.__session is None:
            raise RuntimeError("UOW session is not initialized. Use 'async with BaseUOW()'")