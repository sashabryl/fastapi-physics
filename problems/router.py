from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from problems import schemas, models, crud
from dependencies import get_db


router = APIRouter()


@router.post("/themes/", response_model=schemas.Theme)
async def create_theme(
        theme_schema: Annotated[schemas.ThemeCreate, Depends()],
        db: AsyncSession = Depends(get_db)
):
    return await crud.create_theme(db=db, theme_schema=theme_schema)


@router.get("/themes/", )
async def read_themes(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_themes(db=db)


@router.get("/themes/{theme_id}/", response_model=schemas.Theme)
async def read_one_theme(theme_id: int, db: AsyncSession = Depends(get_db)):
    theme = await crud.get_theme_by_id(db=db, theme_id=theme_id)
    if not theme:
        raise HTTPException(
            status_code=404,
            detail=f"Problem with id {theme_id} isn't found(("
        )
    return theme
