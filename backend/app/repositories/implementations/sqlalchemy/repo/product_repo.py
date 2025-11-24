from app.db.models.models import Product
from app.repositories.implementations.sqlalchemy.base_repo import BaseSQLAlchemyRepository
from app.schemas.dto import ProductDTO
from app.repositories.interfaces.abc_repo.abc_product_repo import IProductRepository

class ProductRepository(IProductRepository, BaseSQLAlchemyRepository[ProductDTO, Product]):
    model = Product