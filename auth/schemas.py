from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, ConfigDict, field_validator


class UserBase(BaseModel):
    username: str
    email: EmailStr
    password1: str
    password2: str


    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str):
        if "@" in v:
            raise HTTPException(400, "Username mustn't contain @. It's dangerous")
        if " " in v:
            raise HTTPException(400, "Username mustn't contain spaces. It's dangerous")

        if not (v.isascii() and not v.isdigit() and not v.isalpha()):
            raise HTTPException(
                400,
                "Please make sure that your username is made of "
                "a combination of digits and ascii symbols."
            )
        return v


class UserRegisterResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: EmailStr


class User(UserRegisterResponse):
    score: int
    completions: int


class UserFull(User):
    hash_password: bytes


class UserLogin(BaseModel):
    username_or_email: str
    password: str


class TokenInfo(BaseModel):
    type: str
    access_token: bytes
