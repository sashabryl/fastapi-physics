from fastapi import HTTPException
from sqlalchemy import insert, column
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
    return data
