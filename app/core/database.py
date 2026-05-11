from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

# URL de conexão com o banco de dados PostgreSQL usando asyncpg
DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/meubanco"

engine = create_async_engine(DATABASE_URL)
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)
Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

