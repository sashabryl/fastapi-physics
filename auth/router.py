from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from auth import schemas, crud, utils
from dependencies import get_db


router_jwt = APIRouter(tags=["JWT"])
router_user = APIRouter(tags=["User"])


@router_jwt.post("/login/", response_model=schemas.TokenInfo)
def issue_jwt_access_token(user: schemas.User = Depends(crud.validate_auth_user)):
    jwt_payload = {
        "sub": user.id,
        "username": user.username,
        "email": user.email
    }
    access_token = utils.encode_jwt(payload=jwt_payload)
    return schemas.TokenInfo(type="Bearer", access_token=access_token)


@router_user.post("/", response_model=schemas.UserRegisterResponse)
async def create_user(
    user_schema: schemas.UserBase,
    db: AsyncSession = Depends(get_db)
):
    return await crud.create_user(db=db, user_schema=user_schema)


@router_user.get("/{user_id}/", response_model=schemas.User)
async def get_one_user(user_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_user_by_id(db=db, user_id=user_id)


@router_user.get("/profile/me/", response_model=schemas.User)
async def user_me(user: schemas.User = Depends(crud.get_current_user)):
    if not user:
        raise HTTPException(401, "Authentication error")
    return user
