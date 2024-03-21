from typing import Annotated

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from enums import DifficultyLevel
from database import Base


intpk = Annotated[int, mapped_column(primary_key=True)]


class Theme(Base):
    __tablename__ = "theme"

    id: Mapped[intpk]
    name: Mapped[str]

    problems: Mapped[list["Problem"]] = relationship(back_populates="theme")

    repr_cols = ("id", "name")


class Problem(Base):
    __tablename__ = "problem"

    id: Mapped[intpk]
    name: Mapped[str]
    difficulty_level: Mapped[DifficultyLevel]
    description: Mapped[str]
    answer: Mapped[str]
    explanation: Mapped[str]
    theme_id: Mapped[int | None] = mapped_column(
        ForeignKey("theme.id", ondelete="SET NULL"),
        nullable=True
    )

    theme: Mapped["Theme"] = relationship(back_populates="problems")

    images: Mapped[list["ExplanationImage"]] = relationship(back_populates="problem")

    repr_cols = ("id", "name", "difficulty_level")


class ExplanationImage(Base):
    __tablename__ = "explanation_image"

    id: Mapped[intpk]
    image_url: Mapped[str]
    problem_id: Mapped[int] = mapped_column(
        ForeignKey("problem.id", ondelete="CASCADE"),
    )

    problem: Mapped["Problem"] = relationship(back_populates="images")

    repr_cols = ("id", "problem_id")
