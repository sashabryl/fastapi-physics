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
    theme_id: int


class Problem(ProblemBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    theme: Theme


class ProblemList(ProblemBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    difficulty_level: DifficultyLevel
    theme: Theme


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
