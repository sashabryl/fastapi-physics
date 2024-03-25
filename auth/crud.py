from fastapi import HTTPException
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from auth import schemas, models, utils


def validate_password(password1: str, password2: str) -> None | HTTPException:
    if not password1 == password2:
        raise HTTPException(400, "Passwords do not match.")

    if password1.isalpha() or password1.isdigit():
        raise HTTPException(400, "Password must contain both letters and digits.")

    if not password1.isascii():
        raise HTTPException(400, "Make sure your password consists of ascii characters only.")
    return


async def create_user(db: AsyncSession, user_schema: schemas.UserBase) -> str:
    validate_password(password1=user_schema.password1, password2=user_schema.password2)

    hashed_password = utils.hash_password(user_schema.password1)
    data = user_schema.model_dump(exclude={"password1", "password2"})
    data["hashed_password"] = hashed_password
    stmt = insert(models.User).values(**data).returning(models.User.username)
    result = await db.execute(stmt)
    await db.commit()
    return result.scalars().first()
