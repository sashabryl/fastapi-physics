from typing import Annotated

from fastapi import APIRouter, Depends
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
