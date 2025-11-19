from app.db.models.models import Product
from app.repositories.implementations.sqlalchemy.base_repo import BaseSQLAlchemyRepository
from app.schemas.dto import ProductDTO

class ProductRepository(BaseSQLAlchemyRepository[ProductDTO, Product]):
    model = Product