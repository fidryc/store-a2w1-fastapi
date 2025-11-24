from app.repositories.interfaces.abc_repo.abc_user_repo import IUserRepository
from app.schemas.dto import UserDTO
from app.repositories.implementations.sqlalchemy.base_repo import BaseSQLAlchemyRepository
from app.db.models.models import User


class UserRepository(IUserRepository, BaseSQLAlchemyRepository[UserDTO, User]):
    model = User