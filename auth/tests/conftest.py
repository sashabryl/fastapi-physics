import pytest
from sqlalchemy import delete

from auth.models import User


@pytest.fixture()
async def clear_users(session):
    yield
    stmt = delete(User).where(User.id > 2)
    await session.execute(stmt)
    await session.commit()
