from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import settings

SQLALCHEMY_DATABASE_URL = (
    f"postgresql+aiopg"
    f"://{settings.POSTGRES_USER}"
    f":{settings.POSTGRES_PASSWORD}"
    f"@{settings.POSTGRES_HOST}"
    f":{settings.POSTGRES_PORT}"
    f"/{settings.POSTGRES_DATABASE}"
)

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
