from typing import Annotated, Any

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
