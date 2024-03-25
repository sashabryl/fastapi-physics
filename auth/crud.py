from fastapi import HTTPException
from sqlalchemy import insert, select, column
from sqlalchemy.ext.asyncio import AsyncSession

from auth import schemas, models, utils


def validate_password(password1: str, password2: str) -> None | HTTPException:
    if not password1 == password2:
        raise HTTPException(400, "Passwords do not match.")

    if not len(password1) >= 10:
        raise HTTPException(400, "Make your password 10 or more characters long please.")

    if password1.isalpha() or password1.isdigit():
        raise HTTPException(400, "Password must contain both letters and digits.")

    if not password1.isascii():
        raise HTTPException(400, "Make sure your password consists of ascii characters only.")
    return


async def create_user(db: AsyncSession, user_schema: schemas.UserBase) -> schemas.UserRegisterResponse:
    validate_password(password1=user_schema.password1, password2=user_schema.password2)

    hash_password = utils.hash_password(user_schema.password1)
    data = user_schema.model_dump(exclude={"password1", "password2"})
    data["hash_password"] = hash_password
    stmt = insert(models.User).values(**data).returning(
        column("id"), column("username"), column("email")
    )
    result = await db.execute(stmt)
    user = result.first()
    data = {"id": user[0], "username": user[1], "email": user[2]}
    return schemas.UserRegisterResponse(**data)


async def get_all_users(db: AsyncSession) -> list[schemas.User]:
    stmt = select(models.User)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_user_by_id(db: AsyncSession, user_id: int) -> schemas.User:
    stmt = select(models.User).filter_by(id=user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(404, f"User with id {user_id} is not found")
    return user


async def get_user_by_email_or_username(
        db: AsyncSession,
        email_or_username: str | None
) -> schemas.UserFull | None:

    email_stmt = select(models.User).filter_by(email=email_or_username)
    result = await db.execute(email_stmt)
    email_user = result.scalar_one_or_none()

    username_stmt = select(models.User).filter_by(username=email_or_username)
    result = await db.execute(username_stmt)
    username_user = result.scalar_one_or_none()

    if email_user and username_user:
        if email_user.id == username_user.id:
            return email_user

    if email_user and not username_user:
        return email_user

    if username_user and not email_user:
        return username_user


async def delete_user_by_id(db: AsyncSession, user_id: int):
    user = await get_user_by_id(db=db, user_id=user_id)
    await db.delete(user)
    await db.commit()
    return True
