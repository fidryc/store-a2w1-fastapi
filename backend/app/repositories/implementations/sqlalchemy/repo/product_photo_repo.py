from app.db.models.models import ProductPhoto
from app.repositories.implementations.sqlalchemy.base_repo import BaseSQLAlchemyRepository
from app.schemas.dto import ProductPhotoDTO

class ProductPhotoRepository(BaseSQLAlchemyRepository[ProductPhotoDTO, ProductPhoto]):
    model = ProductPhoto