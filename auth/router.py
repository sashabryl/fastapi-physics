from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from auth import schemas, crud
from dependencies import get_db


router_jwt = APIRouter(tags=["JWT"])
router_user = APIRouter(tags=["User"])


@router_user.post("/", response_model=schemas.UserRegisterResponse)
async def create_user(
    user_schema: Annotated[schemas.UserBase, Depends()],
    db: AsyncSession = Depends(get_db)
):
    return await crud.create_user(db=db, user_schema=user_schema)


@router_user.get("/", response_model=list[schemas.User])
async def read_users(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_users(db=db)


@router_user.get("/{user_id}/", response_model=schemas.User)
async def get_one_user(user_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_user_by_id(db=db, user_id=user_id)


@router_user.delete("/{user-id}/")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.delete_user_by_id(db=db, user_id=user_id)
