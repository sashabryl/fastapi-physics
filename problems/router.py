from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from problems import schemas, crud
from dependencies import get_db


router_theme = APIRouter(tags=["Theme"])
router_problem = APIRouter(tags=["Problem"])


@router_theme.post("/themes/", response_model=schemas.Theme)
async def create_theme(
        theme_schema: Annotated[schemas.ThemeBase, Depends()],
        db: AsyncSession = Depends(get_db)
):
    return await crud.create_theme(db=db, theme_schema=theme_schema)


@router_theme.get("/themes/", )
async def read_themes(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_themes(db=db)


@router_theme.get("/themes/{theme_id}/", response_model=schemas.Theme)
async def read_one_theme(theme_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_theme_by_id(db=db, theme_id=theme_id)


@router_theme.put("/themes/{theme_id}/", response_model=schemas.Theme)
async def update_theme(
        theme_id: int,
        theme_schema: Annotated[schemas.ThemeBase, Depends()],
        db: AsyncSession = Depends(get_db)
):
    return await crud.update_theme(db=db, theme_id=theme_id, theme_schema=theme_schema)


@router_theme.delete("/themes/{theme_id}/", response_model=schemas.Success)
async def delete_theme(theme_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.delete_theme(db=db, theme_id=theme_id)


@router_problem.post("/problems/", response_model=schemas.Problem)
async def create_problem(
        problem_schema: Annotated[schemas.ProblemBase, Depends()],
        db: AsyncSession = Depends(get_db)
):
    return await crud.create_problem(db=db, problem_schema=problem_schema)


@router_problem.get("/problems/{problem_id}/", response_model=schemas.Problem)
async def get_one_problem(problem_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_problem_by_id(db=db, problem_id=problem_id)


@router_problem.get("/problems/", response_model=list[schemas.ProblemList])
async def read_problems(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_problems(db=db)
