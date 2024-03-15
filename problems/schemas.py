from pydantic import BaseModel, ConfigDict

from enums import DifficultyLevel


class ThemeBase(BaseModel):
    name: str


class ThemeCreate(ThemeBase):
    pass


class ThemeList(ThemeBase):
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


class ProblemList(ProblemBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    theme: ThemeBase
