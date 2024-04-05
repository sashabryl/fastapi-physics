from fastapi import HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from auth import crud as auth_crud, models as auth_models
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


async def get_problem_by_id(db: AsyncSession, problem_id: int) -> schemas.Problem:
    stmt = (
        select(models.Problem)
        .options(selectinload(models.Problem.completed_by))
        .options(joinedload(models.Problem.theme))
        .options(selectinload(models.Problem.images))
        .filter_by(id=problem_id)
    )
    result = await db.execute(stmt)
    problem = result.unique().scalars().first()
    if not problem:
        raise HTTPException(
            status_code=404,
            detail=f"Problem with id {problem_id} isn't found(("
        )
    return problem


async def create_problem(
        db: AsyncSession,
        problem_schema: schemas.ProblemBase
) -> schemas.Problem:
    stmt = (
        insert(models.Problem)
        .values(**problem_schema.model_dump())
        .returning(models.Problem.id)
    )
    result = await db.execute(stmt)
    await db.commit()
    problem_id = result.scalars().first()
    return await get_problem_by_id(db=db, problem_id=problem_id)


async def get_all_problems(db: AsyncSession) -> list[schemas.ProblemList]:
    stmt = (
        select(models.Problem)
        .options(joinedload(models.Problem.theme))
        .options(selectinload(models.Problem.images))
        .options(selectinload(models.Problem.completed_by))
    )
    themes = await db.execute(stmt)
    return list(themes.unique().scalars().all())


async def check_problem_answer(
        db: AsyncSession,
        problem_id: int,
        user: auth_models.User,
        answer: schemas.ProblemAnswer,
) -> bool:
    problem = await get_problem_by_id(db=db, problem_id=problem_id)
    if problem.answer == answer.answer:
        if user:
            if user not in problem.completed_by:
                problem.completed_by.append(user)
                await auth_crud.increment_user_score(
                    db=db,
                    user=user,
                    problem_level=problem.difficulty_level.value.lower()
                )
                await db.commit()
        return True
    return False


async def create_explanation_image(problem_id: int, image_url: str, db: AsyncSession) -> schemas.Success:
    stmt = insert(models.ExplanationImage).values(problem_id=problem_id, image_url=image_url)
    await db.execute(stmt)
    await db.commit()
    return schemas.Success()
