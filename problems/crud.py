from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from problems import schemas, models


async def create_theme(db: AsyncSession, theme_schema: schemas.ThemeCreate) -> schemas.Theme:
    db_theme = models.Theme(**theme_schema.model_dump())
    db.add(db_theme)
    await db.commit()

    return db_theme


async def get_all_themes(db: AsyncSession) -> list[schemas.Theme]:
    stmt = select(models.Theme)
    themes = await db.execute(stmt)
    return [schemas.Theme.model_validate(theme) for theme in themes.all()]
