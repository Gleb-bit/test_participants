from os import environ

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

POSTGRES_DB = environ.get("POSTGRES_DB")
POSTGRES_USER = environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = environ.get("POSTGRES_PASSWORD")
POSTGRES_HOST = environ.get("POSTGRES_HOST")
POSTGRES_PORT = environ.get("POSTGRES_PORT")

SECRET_KEY = environ.get("SECRET_KEY")
DATABASE_URL = environ.get("DATABASE_URL")


Base = declarative_base()

engine = create_async_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, future=True)


async def get_session():
    async with SessionLocal() as session:
        yield session
