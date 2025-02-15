from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from database.models import Base
from secret_info import DB_URL

engine = create_async_engine(DB_URL, echo=True)

session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def create_db():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


async def drop_db():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
