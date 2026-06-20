from sqlalchemy import Insert

from app.db.session import session_maker
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.models import User
from app.utils.hashing import get_hash

import asyncio

async def add_admin(email: str, password: str):
    async with session_maker() as session:
        session: AsyncSession = session
        query = Insert(User).values(
            email=email,
            hashed_password=get_hash(password),
            role="admin",
        )
        await session.execute(query)
        await session.commit()
        
def add(email: str, password: str):
    asyncio.run(add_admin(email, password))
