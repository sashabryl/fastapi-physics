from fastapi import HTTPException
from sqlalchemy import select, insert, func, or_, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

import auth.schemas
import enums
from auth import crud as auth_crud, models as auth_models
from problems import schemas, models


async def create_theme(db: AsyncSession, theme_schema: schemas.ThemeBase) -> schemas.Success:
    theme = models.Theme(**theme_schema.model_dump())
    db.add(theme)
    await db.commit()
    await db.refresh(theme)
    return schemas.Success()


async def get_all_themes(db: AsyncSession) -> list[schemas.Theme]:
    stmt = (
        select(models.Theme)
        .options(selectinload(models.Theme.problems))
        .options(selectinload(models.Theme.questions))
    )
    result = await db.execute(stmt)
    themes = list(result.scalars().all())
    for theme in themes:
        theme.problems_num = len(theme.problems)
        theme.questions_num = len(theme.questions)
    return themes


async def get_theme_by_id(db: AsyncSession, theme_id: int) -> schemas.Theme:
    stmt = (
        select(models.Theme)
        .options(selectinload(models.Theme.problems))
        .options(selectinload(models.Theme.questions))
        .filter_by(id=theme_id)
    )
    result = await db.execute(stmt)
    theme = result.scalars().first()
    if not theme:
        raise HTTPException(
            status_code=404,
            detail=f"Theme with id {theme_id} isn't found(("
        )
    theme.problems_num = len(theme.problems)
    theme.questions_num = len(theme.questions)
    return theme


async def get_theme_by_name(name: str, db: AsyncSession) -> schemas.Theme | None:
    stmt = (
        select(models.Theme)
        .options(selectinload(models.Theme.problems))
        .options(selectinload(models.Theme.questions))
        .filter_by(name=name)
    )
    result = await db.execute(stmt)
    return result.scalars().one_or_none()


async def update_theme(
        db: AsyncSession,
        theme_id: int,
        theme_schema: schemas.ThemeBase
) -> schemas.Theme:
    theme = await get_theme_by_id(db=db, theme_id=theme_id)
    theme.name = theme_schema.name
    theme.description = theme_schema.description
    await db.commit()
    await db.refresh(theme)
    return theme


async def delete_theme(db: AsyncSession, theme_id: int) -> schemas.Success:
    theme = await get_theme_by_id(db=db, theme_id=theme_id)
    await db.delete(theme)
    await db.commit()
    return schemas.Success()


async def delete_all_themes(db: AsyncSession) -> None:
    """This is for testing only"""
    stmt = delete(models.Theme)
    await db.execute(stmt)
    await db.commit()


async def get_problem_by_id(db: AsyncSession, problem_id: int) -> schemas.Problem:
    stmt = (
        select(models.Problem)
        .options(selectinload(models.Problem.completed_by))
        .options(selectinload(models.Problem.comments))
        .options(joinedload(models.Problem.theme))
        .options(joinedload(models.Problem.created_by))
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
    problem.completions = len(problem.completed_by)
    if problem.comments:
        problem.comments_num = (
            len(problem.comments) if isinstance(problem.comments, list)
            else len([problem.comments])
        )
    else:
        problem.comments_num = 0
    return problem


async def create_problem(
        db: AsyncSession,
        problem_schema: schemas.ProblemCreate,
        author: auth_models.User
) -> schemas.Success:
    if not author:
        raise HTTPException(401, "Authentication error")
    if not author.score >= 100 and not author.is_superuser:
        raise HTTPException(
            403,
            "Your score needs to be 100 or higher "
            "before you can create your own problems"
        )
    theme = await get_theme_by_id(db=db, theme_id=problem_schema.theme_id)
    if not theme:
        raise HTTPException(400, f"Theme with id {problem_schema.theme_id} does not exist!")
    stmt = (
        insert(models.Problem)
        .values(**problem_schema.model_dump(), author_id=author.id)
    )
    await db.execute(stmt)
    await db.commit()
    return schemas.Success()


async def get_all_problems(
        offset: int,
        limit: int,
        theme_id: int | None,
        keywords: str | None,
        db: AsyncSession
) -> list[schemas.ProblemList]:
    stmt = (
        select(models.Problem)
        .options(joinedload(models.Problem.theme))
        .options(selectinload(models.Problem.comments))
        .options(joinedload(models.Problem.created_by))
        .options(selectinload(models.Problem.images))
        .options(selectinload(models.Problem.completed_by))
        .offset(offset)
        .limit(limit)
    )
    if theme_id is not None:
        stmt = stmt.where(models.Problem.theme.has(models.Theme.id == theme_id))
    if keywords is not None:
        keywords_ls = keywords.split(" ")
        clauses = [models.Problem.description.icontains(keyword) for keyword in keywords_ls]
        stmt = stmt.where(or_(*clauses))
    result = await db.execute(stmt)
    problems = list(result.unique().scalars().all())
    for problem in problems:
        problem.completions = len(problem.completed_by)
    return problems


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
    else:
        return False


async def create_explanation_image(
        problem_id: int, image_url: str, db: AsyncSession
) -> schemas.Success:
    stmt = insert(models.ExplanationImage).values(problem_id=problem_id, image_url=image_url)
    await db.execute(stmt)
    await db.commit()
    return schemas.Success()


async def delete_problem(
        problem_id: int, user: auth_models.User, db: AsyncSession
) -> schemas.Success:
    problem = await get_problem_by_id(db=db, problem_id=problem_id)
    if not user.is_superuser and not problem.created_by == user:
        raise HTTPException(403, "You do not have permission to do this")
    await db.delete(problem)
    await db.commit()
    return schemas.Success()


async def create_comment(
        problem_id: int,
        user: auth_models.User,
        body: str,
        db: AsyncSession
) -> schemas.Success:
    problem = await get_problem_by_id(db=db, problem_id=problem_id)
    stmt = insert(models.Comment).values(
        author_id=user.id,
        problem_id=problem_id,
        body=body
    )
    await db.execute(stmt)
    await db.commit()
    await db.refresh(problem)
    return schemas.Success()


async def get_all_comments(problem_id: int, db: AsyncSession) -> list[schemas.Comment]:
    stmt = (
        select(models.Comment)
        .options(selectinload(models.Comment.responses))
        .options(joinedload(models.Comment.problem))
        .options(joinedload(models.Comment.created_by))
        .filter_by(problem_id=problem_id)
        .order_by(models.Comment.created_at.desc())
    )
    result = await db.execute(stmt)
    return list(result.unique().scalars().all())


async def get_comment_by_id(comment_id: int, db: AsyncSession) -> models.Comment | None:
    stmt = (
        select(models.Comment)
        .options(selectinload(models.Comment.responses))
        .options(joinedload(models.Comment.problem))
        .options(joinedload(models.Comment.created_by))
        .filter_by(id=comment_id)
    )
    result = await db.execute(stmt)
    return result.unique().scalars().one_or_none()


async def get_comment_reaction(
        user_id: int,
        comment_id: int,
        belongs_to: enums.ReactionOwner,
        db: AsyncSession
) -> models.CommentReaction | None:
        stmt = (
            select(models.CommentReaction)
            .filter_by(
                user_id=user_id,
                comment_id=comment_id,
                belongs_to=belongs_to
            )
        )
        result = await db.execute(stmt)
        return result.unique().scalars().one_or_none()


async def create_comment_reaction(
        user_id: int,
        comment_id: int,
        type: enums.ReactionType,
        belongs_to: enums.ReactionOwner,
        db: AsyncSession
) -> None:
    stmt = (
        insert(models.CommentReaction)
        .values(
            user_id=user_id,
            comment_id=comment_id,
            type=type,
            belongs_to=belongs_to
        )
    )
    await db.execute(stmt)


async def like_comment(
        comment: models.Comment,
        comment_type: enums.ReactionOwner,
        user: auth_models.User,
        db: AsyncSession
) -> None:
    comment_reaction = await get_comment_reaction(
        user_id=user.id,
        comment_id=comment.id,
        belongs_to=comment_type,
        db=db
    )
    if not comment_reaction:
        await create_comment_reaction(
            user_id=user.id,
            comment_id=comment.id,
            type=enums.ReactionType.LIKE,
            belongs_to=comment_type,
            db=db
        )
        comment.likes += 1
        await db.commit()
        await db.refresh(comment)
        return

    if comment_reaction.type == enums.ReactionType.LIKE:
        return

    if comment_reaction.type == enums.ReactionType.DISLIKE:
        await db.delete(comment_reaction)
        await create_comment_reaction(
            comment_id=comment.id,
            user_id=user.id,
            type=enums.ReactionType.LIKE,
            belongs_to=comment_type,
            db=db
        )
        comment.dislikes -= 1
        comment.likes += 1
        await db.commit()
        await db.refresh(comment)


async def dislike_comment(
        comment: models.Comment,
        comment_type: enums.ReactionOwner,
        user: auth_models.User,
        db: AsyncSession
) -> None:
    comment_reaction = await get_comment_reaction(
        user_id=user.id,
        comment_id=comment.id,
        belongs_to=comment_type,
        db=db
    )

    if not comment_reaction:
        await create_comment_reaction(
            user_id=user.id,
            comment_id=comment.id,
            type=enums.ReactionType.DISLIKE,
            belongs_to=comment_type,
            db=db
        )
        comment.dislikes += 1
        await db.commit()
        await db.refresh(comment)
        return

    if comment_reaction.type == enums.ReactionType.DISLIKE:
        return

    if comment_reaction.type == enums.ReactionType.LIKE:
        await db.delete(comment_reaction)
        await create_comment_reaction(
            user_id=user.id,
            comment_id=comment.id,
            type=enums.ReactionType.DISLIKE,
            belongs_to=comment_type,
            db=db
        )
        comment.likes -= 1
        comment.dislikes += 1
        await db.commit()
        await db.refresh(comment)
        return


async def create_comment_response(
        body: str,
        user: auth_models.User,
        comment: models.Comment,
        db: AsyncSession
) -> schemas.Success:
    stmt = insert(models.CommentResponse).values(
        body=body, author_id=user.id, comment_id=comment.id
    )
    await db.execute(stmt)
    await db.commit()
    await db.refresh(comment)
    return schemas.Success()


async def get_all_comment_responses(
        comment: models.Comment, db: AsyncSession
) -> list[schemas.Comment]:
    stmt = (
        select(models.CommentResponse)
        .options(joinedload(models.CommentResponse.comment))
        .options(joinedload(models.CommentResponse.created_by))
        .filter_by(comment_id=comment.id)
        .order_by(models.CommentResponse.created_at.desc())
    )
    result = await db.execute(stmt)
    return list(result.unique().scalars().all())


async def get_comment_response_by_id(response_id: int, db: AsyncSession) -> schemas.Comment:
    stmt = (
        select(models.CommentResponse)
        .options(joinedload(models.CommentResponse.comment))
        .options(joinedload(models.CommentResponse.created_by))
        .filter_by(id=response_id)
    )
    result = await db.execute(stmt)
    return result.unique().scalars().one_or_none()


async def create_question(
        question_schema: schemas.QuestionBase,
        author_id: int,
        db: AsyncSession
) -> schemas.Success:
    stmt = (
        insert(models.Question)
        .values(**question_schema.model_dump(), author_id=author_id)
    )
    await db.execute(stmt)
    await db.commit()
    return schemas.Success()


async def get_all_questions(
        offset: int,
        limit: int,
        theme_id: int | None,
        keywords: str | None,
        db: AsyncSession
) -> list[schemas.QuestionList]:
    stmt = (
        select(models.Question)
        .options(joinedload(models.Question.created_by))
        .options(joinedload(models.Question.theme))
        .options(selectinload(models.Question.responses))
        .offset(offset)
        .limit(limit)
        .order_by(models.Question.created_at.desc())
    )
    if theme_id is not None:
        stmt = stmt.filter_by(theme_id=theme_id)
    if keywords is not None:
        keywords_ls = keywords.split(" ")
        clauses = [models.Question.description.icontains(keyword) for keyword in keywords_ls]
        clauses.extend(models.Question.title.icontains(keyword) for keyword in keywords_ls)
        stmt = stmt.where(or_(*clauses))
    result = await db.execute(stmt)
    questions = result.unique().scalars().all()
    return list(questions)


async def get_question_by_id(question_id: int, db: AsyncSession) -> schemas.Question:
    stmt = (
        select(models.Question)
        .options(joinedload(models.Question.created_by))
        .options(joinedload(models.Question.theme))
        .options(selectinload(models.Question.responses))
    )
    result = await db.execute(stmt)
    question = result.unique().scalars().first()
    if not question:
        raise HTTPException(404, f"Question with id {question_id} not found.")
    return question


async def create_question_response(
        body: str,
        question: models.Question,
        author: auth_models.User,
        db: AsyncSession
) -> schemas.Success:
    stmt = (
        insert(models.QuestionResponse)
        .values(question_id=question.id, author_id=author.id, body=body)
    )
    await db.execute(stmt)
    await db.commit()
    return schemas.Success()


async def get_all_question_responses(question_id: int, db: AsyncSession) -> list[schemas.Comment]:
    stmt = (
        select(models.QuestionResponse)
        .options(joinedload(models.QuestionResponse.question))
        .options(joinedload(models.QuestionResponse.created_by))
        .filter_by(id=question_id)
        .order_by(models.QuestionResponse.created_at)
    )
    result = await db.execute(stmt)
    questions = result.unique().scalars().all()
    return questions


async def get_question_response_by_id(question_response_id: int, db: AsyncSession) -> schemas.Comment:
    stmt = (
        select(models.QuestionResponse)
        .options(joinedload(models.QuestionResponse.question))
        .options(joinedload(models.QuestionResponse.created_by))
        .filter_by(id=question_response_id)
    )
    result = await db.execute(stmt)
    return result.unique().scalars().first()
