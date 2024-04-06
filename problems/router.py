from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

import auth.crud
from problems import schemas, crud
from dependencies import get_db
from aws import utils
from auth.crud import get_current_user


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
        problem_schema: Annotated[schemas.ProblemCreate, Depends()],
        db: AsyncSession = Depends(get_db),
        author = Depends(auth.crud.get_current_user)
):
    return await crud.create_problem(db=db, problem_schema=problem_schema, author=author)


@router_problem.get("/problems/{problem_id}/", response_model=schemas.Problem)
async def get_one_problem(problem_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_problem_by_id(db=db, problem_id=problem_id)


@router_problem.get("/problems/", response_model=list[schemas.ProblemList])
async def read_problems(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_problems(db=db)


@router_problem.post("/problems/{problem_id}/submit/", response_model=schemas.Success)
async def submit_problem_solution(
    problem_id: int,
    answer: Annotated[schemas.ProblemAnswer, Depends()],
    user = Depends(auth.crud.get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await crud.check_problem_answer(
        db=db, problem_id=problem_id, user=user, answer=answer
    )

    return schemas.Success(success=result)


@router_problem.post("/problems/{problem_id}/upload-image/", response_model=schemas.Success)
async def upload_explanation_image(
        problem_id: int,
        image: UploadFile,
        db: Annotated[AsyncSession, Depends(get_db)]
):
    directory = "explanations"
    image_url = await utils.upload_image(file=image, directory=directory)
    result = await crud.create_explanation_image(
        problem_id=problem_id, image_url=image_url, db=db
    )
    return result


@router_problem.get(
    "/problems/{problem_id}/explanation/",
    response_model=schemas.ProblemExplanation
)
async def read_problem_explanation(
        problem_id: int,
        db: Annotated[AsyncSession, Depends(get_db)]
):
    return await crud.get_problem_by_id(db=db, problem_id=problem_id)


@router_problem.delete("/problems/{problem_id}/", response_model=schemas.Success)
async def delete_problem(
        problem_id: int,
        db: AsyncSession = Depends(get_db),
        user = Depends(auth.crud.get_current_user)
):
    return await crud.delete_problem(problem_id=problem_id, db=db, user=user)
