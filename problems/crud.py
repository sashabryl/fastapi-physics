from fastapi import HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from problems import schemas, models


async def create_theme(db: AsyncSession, theme_schema: schemas.ThemeBase) -> schemas.Theme:
    theme = models.Theme(**theme_schema.model_dump())
    db.add(theme)
    await db.commit()
    await db.refresh(theme)
    return theme


async def get_all_themes(db: AsyncSession) -> list[schemas.Theme]:
    stmt = (
        select(models.Theme)
        .options(
            selectinload(models.Theme.problems)
        )
    )
    themes = await db.execute(stmt)
    return list(themes.scalars().all())


async def get_theme_by_id(db: AsyncSession, theme_id: int) -> schemas.Theme:
    stmt = (
        select(models.Theme)
        .options(
            selectinload(models.Theme.problems)
        ).filter_by(id=theme_id)
    )
    result = await db.execute(stmt)
    theme = result.scalars().first()
    if not theme:
        raise HTTPException(
            status_code=404,
            detail=f"Problem with id {theme_id} isn't found(("
        )
    return theme


async def update_theme(
        db: AsyncSession,
        theme_id: int,
        theme_schema: schemas.ThemeBase
) -> schemas.Theme:
    theme = await get_theme_by_id(db=db, theme_id=theme_id)
    theme.name = theme_schema.name
    await db.commit()
    await db.refresh(theme)
    return theme


async def delete_theme(db: AsyncSession, theme_id: int) -> schemas.Success:
    theme = await get_theme_by_id(db=db, theme_id=theme_id)
    await db.delete(theme)
    await db.commit()
    return schemas.Success()
