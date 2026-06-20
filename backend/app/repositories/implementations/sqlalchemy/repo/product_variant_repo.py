from sqlalchemy import text
from app.db.models.models import ProductVariant
from app.repositories.implementations.sqlalchemy.base_repo import BaseSQLAlchemyRepository
from app.schemas.dto import ColorDTO, ProductVariantDTO, SizeDTO
from app.repositories.interfaces.abc_repo.abc_product_variant_repo import IProductVariantRepository

class ProductVariantRepository(IProductVariantRepository, BaseSQLAlchemyRepository[ProductVariantDTO, ProductVariant]):
    model = ProductVariant
    
    async def size_variation_of_product(self, product_id: int) -> list[SizeDTO]:
        query = text(
            """
            SELECT DISTINCT sizes.id, sizes.title
            FROM product_variants
            LEFT JOIN sizes ON product_variants.size_id = sizes.id
            WHERE product_variants.product_id = :product_id
            """
        )
        res = (await self.session.execute(query, params={"product_id": product_id}))
        size_dtos = [SizeDTO.model_construct(**obj) for obj in res.mappings().all()]
        return size_dtos
    
    async def color_variation_of_product(self, product_id: int) -> list[ColorDTO]:
        query = text("""
                     SELECT DISTINCT colors.id, colors.title, colors.hex_code
                    FROM product_variants
                    LEFT JOIN sizes ON product_variants.size_id = sizes.id
                    WHERE product_variants.product_id = :product_id
                    """
                     )
        res = (await self.session.execute(query, params={"product_id": product_id}))
        color_dtos = [ColorDTO.model_construct(**obj) for obj in res.mappings().all()]
        return color_dtos