from app.db.models.models import ProductVariant
from app.repositories.implementations.sqlalchemy.base_repo import BaseSQLAlchemyRepository
from app.schemas.dto import ProductVariantDTO

class ProductVariantRepository(BaseSQLAlchemyRepository[ProductVariantDTO, ProductVariant]):
    model = ProductVariant