from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

import auth.crud
import enums
from problems import schemas, crud
from dependencies import get_db
from aws import utils
from auth.crud import get_current_user


router_theme = APIRouter(tags=["Theme"])
router_problem = APIRouter(tags=["Problem"])


@router_theme.post("/themes/", response_model=schemas.Success)
async def create_theme(
        theme_schema: Annotated[schemas.ThemeBase, Depends()],
        db: AsyncSession = Depends(get_db)
):
    theme_with_same_name = await crud.get_theme_by_name(name=theme_schema.name, db=db)
    if theme_with_same_name:
        raise HTTPException(400, f"Theme with name {theme_schema.name} already exists!")
    return await crud.create_theme(db=db, theme_schema=theme_schema)


@router_theme.get("/themes/", response_model=list[schemas.Theme])
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
        author = Depends(get_current_user)
):
    return await crud.create_problem(db=db, problem_schema=problem_schema, author=author)


@router_problem.get("/problems/{problem_id}/", response_model=schemas.Problem)
async def get_one_problem(problem_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_problem_by_id(db=db, problem_id=problem_id)


@router_problem.get("/problems/", response_model=list[schemas.ProblemList])
async def read_problems(
        theme_id: int = None,
        offset: int = Query(0, ge=0),
        limit: int = Query(100, ge=0),
        keywords: str = None,
        db: AsyncSession = Depends(get_db)
):
    return await crud.get_all_problems(offset=offset, limit=limit, theme_id=theme_id, keywords=keywords, db=db)


@router_problem.post("/problems/{problem_id}/submit/", response_model=schemas.Success)
async def submit_problem_solution(
    problem_id: int,
    answer: Annotated[schemas.ProblemAnswer, Depends()],
    user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await crud.check_problem_answer(
        db=db, problem_id=problem_id, user=user, answer=answer
    )

    return schemas.Success(success=result)


@router_problem.post(
    "/problems/{problem_id}/upload-images/",
    response_model=schemas.Success
)
async def upload_explanation_images(
        problem_id: int,
        images: list[UploadFile],
        db: Annotated[AsyncSession, Depends(get_db)],
        user = Depends(get_current_user)
):
    if not user:
        raise HTTPException(401, "Authentication error")
    problem = await crud.get_problem_by_id(db=db, problem_id=problem_id)
    if not user == problem.created_by:
        raise HTTPException(403, "You cannot do this, I'm sorry")

    directory = "explanations"
    for image in images:
        image_url = await utils.upload_image(file=image, directory=directory)
        await crud.create_explanation_image(
            problem_id=problem_id, image_url=image_url, db=db
        )
    return schemas.Success


@router_problem.get(
    "/problems/{problem_id}/explanation/",
    response_model=schemas.ProblemExplanation
)
async def read_problem_explanation(
        problem_id: int,
        db: Annotated[AsyncSession, Depends(get_db)]
):
    return await crud.get_problem_by_id(db=db, problem_id=problem_id)


@router_problem.post("/problems/{problem_id}/comments/", response_model=schemas.Success)
async def create_comment(
        problem_id: int,
        body: str,
        user = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    if not user:
        raise HTTPException(401, "Authentication error")
    return await crud.create_comment(problem_id=problem_id, body=body, user=user, db=db)


@router_problem.get("/problems/{problem_id}/comments/", response_model=list[schemas.Comment])
async def read_comments(
        problem_id: int,
        user = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    problem = await crud.get_problem_by_id(db=db, problem_id=problem_id)
    if problem not in user.completed_problems:
        raise HTTPException(403, "First complete this problem!")
    return await crud.get_all_comments(problem_id=problem.id, db=db)


@router_problem.delete("/problems/{problem_id}/", response_model=schemas.Success)
async def delete_problem(
        problem_id: int,
        db: AsyncSession = Depends(get_db),
        user = Depends(get_current_user)
):
    if not user:
        raise HTTPException(401, "Authentication error")
    return await crud.delete_problem(problem_id=problem_id, db=db, user=user)


@router_problem.post(
    "/problems/{problem_id}/comments/{comment_id}/like/",
    response_model=schemas.Success
)
async def like_comment(
        problem_id: int,
        comment_id: int,
        user = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    if not user:
        raise HTTPException(401, "Authentication error")
    if not user.score >= 20:
        raise HTTPException(
            403, "Your score needs to be 20 or higher before you can like anything"
        )
    comment = await crud.get_comment_by_id(comment_id=comment_id, db=db)
    await crud.like_comment(
        comment=comment, comment_type=enums.ReactionOwner.COMMENT, user=user, db=db
    )
    return schemas.Success


@router_problem.post(
    "/problems/{problem_id}/comments/{comment_id}/dislike/",
    response_model=schemas.Success
)
async def dislike_comment(
    problem_id: int,
    comment_id: int,
    user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if not user:
        raise HTTPException(401, "Authentication error")
    if not user.score >= 100:
        raise HTTPException(
            403, "Your score needs to be 100 or higher before you can start complaining"
        )
    comment = await crud.get_comment_by_id(comment_id=comment_id, db=db)
    await crud.dislike_comment(
        comment=comment, comment_type=enums.ReactionOwner.COMMENT, user=user, db=db
    )
    return schemas.Success


@router_problem.post(
    "/problems/{problem_id}/comments/{comment_id}/responses/",
    response_model=schemas.Success
)
async def create_comment_response(
    problem_id: int,
    comment_id: int,
    body: str,
    user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if not user:
        raise HTTPException(401, "Authentication error")
    comment = await crud.get_comment_by_id(comment_id=comment_id, db=db)
    return await crud.create_comment_response(body=body, user=user, comment=comment, db=db)


@router_problem.get(
    "/problems/{problem_id}/comments/{comment_id}/responses/",
    response_model=list[schemas.Comment]
)
async def read_comment_responses(
        problem_id: int,
        comment_id: int,
        db: AsyncSession = Depends(get_db)
):
    comment = await crud.get_comment_by_id(comment_id=comment_id, db=db)
    return await crud.get_all_comment_responses(comment=comment, db=db)


@router_problem.post(
    "/problems/{problem_id}/comments/{comment_id}/responses/{response_id}/like/",
    response_model=schemas.Success
)
async def like_comment_response(
        problem_id: int,
        comment_id: int,
        response_id: int,
        user = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    if not user:
        raise HTTPException(401, "Authentication error")
    if not user.score >= 20:
        raise HTTPException(
            403, "Your score needs to be 20 or higher before you can like anything"
        )
    comment_response = await crud.get_comment_response_by_id(response_id=response_id, db=db)
    await crud.like_comment(
        comment=comment_response, comment_type=enums.ReactionOwner.RESPONSE, user=user, db=db
    )
    return schemas.Success


@router_problem.post(
    "/problems/{problem_id}/comments/{comment_id}/responses/{response_id}/dislike/",
    response_model=schemas.Success
)
async def dislike_comment_response(
        problem_id: int,
        comment_id: int,
        response_id: int,
        user = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    if not user:
        raise HTTPException(401, "Authentication error")
    if not user.score >= 20:
        raise HTTPException(
            403, "Your score needs to be 20 or higher before you can like anything"
        )
    comment_response = await crud.get_comment_response_by_id(response_id=response_id, db=db)
    await crud.dislike_comment(
        comment=comment_response, comment_type=enums.ReactionOwner.RESPONSE, user=user, db=db
    )
    return schemas.Success
