from sqlalchemy import select
from sqlalchemy.orm import joinedload
from app.db.models.models import Product, ProductPhoto
from app.repositories.implementations.sqlalchemy.base_repo import BaseSQLAlchemyRepository
from app.schemas.dto import ProductDTO, ProductWithPhotoDTO
from app.repositories.interfaces.abc_repo.abc_product_repo import IProductRepository
from sqlalchemy.exc import SQLAlchemyError
from app.core.logger import logger
from app.repositories.exceptions.base_exc import RepositoryExc
from app.repositories.utils.serializer import Serializer

class ProductRepository(IProductRepository, BaseSQLAlchemyRepository[ProductDTO, Product]):
    model = Product
    
    async def products_with_photo_by_filters(self, **filters) -> ProductWithPhotoDTO:
        try:
            query = select(
                self.model
            ).where(
                *[getattr(self.model, k) == v for k, v in filters.items()]
            ).options(
                joinedload(self.model.photos).joinedload(ProductPhoto.photo)
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