from app.utils.hashing import get_hash
from app.db.session import session_maker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert
from app.db.models.models import User


async def create_admin(email: str, pwd: str):
    hashed_password = get_hash(pwd)
    async with session_maker() as session:
        session: AsyncSession
        query = insert(User).values(email=email, hashed_password=hashed_password)
        await session.execute(query)
        await session.commit()