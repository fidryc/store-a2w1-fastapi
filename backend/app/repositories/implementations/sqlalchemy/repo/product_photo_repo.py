from app.db.models.models import ProductPhoto
from app.repositories.implementations.sqlalchemy.base_repo import BaseSQLAlchemyRepository
from app.schemas.dto import ProductPhotoDTO
from app.repositories.interfaces.abc_repo.abc_product_photo_repo import IProductPhotoRepository

class ProductPhotoRepository(IProductPhotoRepository, BaseSQLAlchemyRepository[ProductPhotoDTO, ProductPhoto]):
    model = ProductPhoto