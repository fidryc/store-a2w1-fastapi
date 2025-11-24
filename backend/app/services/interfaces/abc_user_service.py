from typing import Protocol


class IUserService(Protocol):
    async def register(email: str, password: str):
        ...