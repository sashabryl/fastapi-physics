from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
    username: str
    email: EmailStr
    password1: str
    password2: str


class UserRegisterResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: EmailStr


class User(UserRegisterResponse):
    score: int


class UserFull(User):
    hash_password: bytes


class UserLogin(BaseModel):
    username_or_email: str
    password: str
