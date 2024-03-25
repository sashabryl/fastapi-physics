from fastapi import HTTPException, Form, Depends
from sqlalchemy import insert, select, column
from sqlalchemy.ext.asyncio import AsyncSession

import dependencies
from auth import schemas, models, utils
from auth.utils import validate_password_registration, validate_password


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


async def get_user_by_email(db: AsyncSession, email: str) -> None | models.User:
    stmt = select(models.User).filter_by(email=email)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_user_by_username(db: AsyncSession, username: str) -> None | models.User:
    stmt = select(models.User).filter_by(username=username)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_user_by_email_or_username(
        db: AsyncSession,
        email_or_username: str | None
) -> schemas.UserFull | None:
    email_user = await get_user_by_email(db=db, email=email_or_username)
    username_user = await get_user_by_username(db=db, username=email_or_username)

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


async def create_user(db: AsyncSession, user_schema: schemas.UserBase) -> schemas.UserRegisterResponse:
    validate_password_registration(password1=user_schema.password1, password2=user_schema.password2)

    if await get_user_by_username(db, user_schema.username):
        raise HTTPException(400, f"User with username {user_schema.username} already exists")

    if await get_user_by_email(db, user_schema.email):
        raise HTTPException(400, f"User with email {user_schema.email} already exists")

    hash_password = utils.hash_password(user_schema.password1)
    data = user_schema.model_dump(exclude={"password1", "password2"})
    data["hash_password"] = hash_password
    stmt = insert(models.User).values(**data).returning(
        column("id"), column("username"), column("email")
    )
    result = await db.execute(stmt)
    await db.commit()
    user = result.first()
    data = {"id": user[0], "username": user[1], "email": user[2]}
    return schemas.UserRegisterResponse(**data)


async def validate_auth_user(
        db: AsyncSession = Depends(dependencies.get_db),
        username_or_email: str = Form(),
        password: str = Form(),
) -> schemas.User:
    auth_exc = HTTPException(401, "Invalid credentials")
    user = await get_user_by_email_or_username(db=db, email_or_username=username_or_email)
    if not user:
        raise auth_exc
    if not validate_password(password, user.hash_password):
        raise auth_exc

    return user
