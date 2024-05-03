import pytest

from problems.crud import create_theme, delete_all_themes
from problems.schemas import ThemeBase
from database import SessionLocal


@pytest.fixture()
async def create_themes():
    async with SessionLocal() as db:
        await create_theme(
            db=db, theme_schema=ThemeBase(name="Mechanics", description="Cool")
        )
        await create_theme(
            db=db, theme_schema=ThemeBase(name="Electronics", description="Whah")
        )


@pytest.fixture()
async def delete_themes():
    yield
    async with SessionLocal() as db:
        await delete_all_themes(db=db)