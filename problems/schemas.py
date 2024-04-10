import datetime

from pydantic import BaseModel, ConfigDict, field_validator

import auth.schemas
from enums import DifficultyLevel


class ThemeBase(BaseModel):
    name: str


class Theme(ThemeBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class ProblemCreate(BaseModel):
    name: str
    difficulty_level: DifficultyLevel
    description: str
    theme_id: int
    answer: str
    explanation: str


class Problem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    theme: Theme
    name: str
    difficulty_level: DifficultyLevel
    description: str
    created_by: auth.schemas.User
    completions: int


class ProblemList(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    theme: Theme
    name: str
    difficulty_level: DifficultyLevel
    created_by: auth.schemas.User
    completions: int


class ProblemAnswer(BaseModel):
    answer: str


class Success(BaseModel):
    success: bool = True


class ExplanationImage(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    image_url: str


class ProblemExplanation(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    difficulty_level: DifficultyLevel
    theme: Theme
    answer: str
    explanation: str
    images: list[ExplanationImage]


class Comment(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_by: auth.schemas.User
    problem: ProblemList
    body: str
    created_at: datetime.datetime

    @field_validator("created_at")
    @classmethod
    def validate_username(cls, v: datetime.datetime):
        return v.strftime("%Y/%m/%d, %H:%M")