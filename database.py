from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

import settings

SQLALCHEMY_DATABASE_URL = settings.POSTGRES_DATABASE_URL

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,
    pool_size=5,
    max_overflow=10,
)
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):

    repr_cols = tuple()

    def __repr__(self):
        cols = [
            f"{col}={getattr(self, col)}"
            for col in self.__table__.columns.keys()
            if col in self.repr_cols
        ]
        return f"<{self.__class__.__name__}, {', '.join(cols)}>"
