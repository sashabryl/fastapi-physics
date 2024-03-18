from pydantic import BaseModel, ConfigDict

from enums import DifficultyLevel


class ThemeBase(BaseModel):
    name: str


class Theme(ThemeBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class ProblemBase(BaseModel):
    name: str
    difficulty_level: DifficultyLevel
    description: str
    answer: str
    explanation: str


class ProblemCreateUpdate(ProblemBase):
    theme_id: int


class Problem(ProblemBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    theme: ThemeBase


class Success(BaseModel):
    success: bool = True
