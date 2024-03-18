from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from problems import schemas, models


async def create_theme(db: AsyncSession, theme_schema: schemas.ThemeCreate) -> schemas.Theme:
    theme = models.Theme(**theme_schema.model_dump())
    db.add(theme)
    await db.commit()
    await db.refresh(theme)
    return theme


async def get_all_themes(db: AsyncSession) -> list[schemas.Theme]:
    stmt = select(models.Theme).options(selectinload(models.Theme.problems))
    themes = await db.execute(stmt)
    return list(themes.scalars().all())
