from typing import Protocol

from app.schemas.dataclasses import AuthTokens
from app.schemas.dto import UserDTO


class IUserService(Protocol):
    async def login(self, email: str, pwd: str) -> AuthTokens: ...
    
    async def refresh_tokens(self, auth_tokens: AuthTokens) -> AuthTokens: ...
    
    async def get_user_from_token(self, auth_tokens: AuthTokens) -> UserDTO: ...
    
    async def register(email: str, pwd: str) -> None:
        ...