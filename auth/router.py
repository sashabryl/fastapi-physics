from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from auth import schemas, crud
from dependencies import get_db


router = APIRouter(tags=["JWT"])


@router.post("/register/", response_model=schemas.UserRegisterResponse)
async def create_user(
    user_schema: Annotated[schemas.UserBase, Depends()],
    db: AsyncSession = Depends(get_db)
):
    return await crud.create_user(db=db, user_schema=user_schema)
