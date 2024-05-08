import pytest

from problems.crud import create_theme, delete_all_themes, delete_all_problems
from problems.schemas import ThemeBase


@pytest.fixture(scope="session", autouse=True)
async def create_themes(session):
    await create_theme(
        db=session, theme_schema=ThemeBase(name="Mechanics", description="Cool")
    )
    await create_theme(
        db=session, theme_schema=ThemeBase(name="Electronics", description="Whah")
    )


@pytest.fixture(scope="session", autouse=True)
async def delete_themes(session):
    yield
    await delete_all_themes(db=session)


@pytest.fixture(scope="session", autouse=True)
async def delete_problems(session):
    yield
    await delete_all_problems(db=session)
