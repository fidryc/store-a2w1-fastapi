from typing import Protocol, TypeVar, Generic

from app.repositories.interfaces.abc_repo.abc_base_category_repo import IBaseCategoryRepository
from app.repositories.interfaces.abc_repo.abc_collection_product_repo import ICollectionProductRepository
from app.repositories.interfaces.abc_repo.abc_collection_repo import ICollectionRepository
from app.repositories.interfaces.abc_repo.abc_color_repo import IColorRepository
from app.repositories.interfaces.abc_repo.abc_material_repo import IMaterialRepository
from app.repositories.interfaces.abc_repo.abc_product_photo_repo import IProductPhotoRepository
from app.repositories.interfaces.abc_repo.abc_product_repo import IProductRepository
from app.repositories.interfaces.abc_repo.abc_product_variant_repo import IProductVariantRepository
from app.repositories.interfaces.abc_repo.abc_size_repo import ISizeRepository
from app.repositories.interfaces.abc_repo.abc_sub_category_repo import ISubCategoryRepository

from typing_extensions import Self

class IBaseUOW(Protocol):
    def __init__(self):
        self.__size_repo: ISizeRepository | None = None
        self.__material_repo: IMaterialRepository | None = None
        self.__color_repo: IColorRepository | None = None
        self.__base_category_repo: IBaseCategoryRepository | None = None
        self.__sub_category_repo: ISubCategoryRepository | None = None
        self.__product_repo: IProductRepository | None = None
        self.__product_variant_repo: IProductVariantRepository | None = None
        self.__collection_repo: ICollectionRepository | None = None
        self.__collection_product_repo: ICollectionProductRepository | None = None
        self.__product_photo_repo: IProductPhotoRepository | None = None


    async def __aenter__(self) -> Self: ...
    
    async def __aexit__(self) -> None: ...
    
    async def rollback(self) -> None: ...
    
    async def commit(self) -> None: ...
    
    async def close(self) -> None: ...
    
    @property
    def size_repo(self): ...

    @property
    def material_repo(self): ...

    @property
    def color_repo(self): ...

    @property
    def base_category_repo(self): ...

    @property
    def sub_category_repo(self): ...

    @property
    def product_repo(self): ...

    @property
    def product_variant_repo(self): ...

    @property
    def collection_repo(self): ...

    @property
    def collection_product_repo(self): ...

    @property
    def product_photo_repo(self): ...
