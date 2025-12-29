from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload
from app.db.models.models import Collection, Product, ProductPhoto
from app.repositories.implementations.sqlalchemy.base_repo import BaseSQLAlchemyRepository
from app.schemas.dto import ProductDTO, ProductWithCategoriesDTO, ProductWithCollectionDTO, ProductWithPhotoDTO
from app.repositories.interfaces.abc_repo.abc_product_repo import IProductRepository
from sqlalchemy.exc import SQLAlchemyError
from app.core.logger import logger
from app.repositories.exceptions.base_exc import RepositoryExc
from app.repositories.utils.serializer import Serializer

class ProductRepository(IProductRepository, BaseSQLAlchemyRepository[ProductDTO, Product]):
    model = Product
    
    async def products_with_photo_by_filters(self, **filters) -> list[ProductWithPhotoDTO]:
        try:
            query = select(
                self.model
            ).where(
                *[getattr(self.model, k) == v for k, v in filters.items()]
            ).options(
                selectinload(self.model.photos).selectinload(ProductPhoto.photo)
                # Загружаем ProductPhoto, затем из него загружаем Photo
            )
            objs = (await self.session.execute(query)).scalars().unique().all()
            return [Serializer.serialize_to_dto(ProductWithPhotoDTO, obj) for obj in objs]
        except SQLAlchemyError as e:
            logger.warning(
                "SQLAlchemyError: failed get by filters products with photo",
                exc_info=True,
                extra={"filters": filters}
            )
            raise RepositoryExc("Failed get by filters") from e
        
    
    async def products_with_categories_by_filters(self, **filters) -> list[ProductWithCategoriesDTO]:
        try:
            query = select(
                self.model
            ).where(
                *[getattr(self.model, k) == v for k, v in filters.items()]
            ).options(
                selectinload(self.model.photos).selectinload(ProductPhoto.photo),
                joinedload(self.model.base_category),
                joinedload(self.model.sub_category)
            )
            objs = (await self.session.execute(query)).scalars().unique().all()
            return [Serializer.serialize_to_dto(ProductWithCategoriesDTO, obj) for obj in objs]
        except SQLAlchemyError as e:
            logger.warning(
                "SQLAlchemyError: failed get by filters products with photo",
                exc_info=True,
                extra={"filters": filters}
            )
            raise RepositoryExc("Failed get by filters") from e
        
    async def products_with_collection(self, **filters) -> list[ProductWithCollectionDTO]:
        try:
            query = select(
                self.model
            ).where(
                *[getattr(self.model, k) == v for k, v in filters.items()]
            ).options(
                selectinload(self.model.photos).selectinload(ProductPhoto.photo),
                joinedload(self.model.collection),
                joinedload(self.model.collection).joinedload(Collection.collection_category),
                joinedload(self.model.collection).joinedload(Collection.photo)
            )
            objs = (await self.session.execute(query)).scalars().unique().all()
            return [Serializer.serialize_to_dto(ProductWithCollectionDTO, obj) for obj in objs]
        except SQLAlchemyError as e:
            logger.warning(
                "SQLAlchemyError: failed get by filters products with photo",
                exc_info=True,
                extra={"filters": filters}
            )
            raise RepositoryExc("Failed get by filters") from e