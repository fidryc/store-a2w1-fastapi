from app.db.models.models import Photo
from app.repositories.implementations.sqlalchemy.base_repo import BaseSQLAlchemyRepository
from app.repositories.interfaces.abc_repo.abc_photo_repo import IPhotoRepository
from app.schemas.dto import PhotoDTO

class PhotoRepository(IPhotoRepository, BaseSQLAlchemyRepository[PhotoDTO, Photo]):
    model = Photo