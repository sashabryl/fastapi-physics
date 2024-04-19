import datetime
from typing import Annotated

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

import enums
from enums import DifficultyLevel
from database import Base


intpk = Annotated[int, mapped_column(primary_key=True)]


class Theme(Base):
    __tablename__ = "theme"

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str] = mapped_column(nullable=False)

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
    author_id: Mapped[int | None] = mapped_column(
        ForeignKey("user.id", ondelete="SET NULL")
    )

    theme: Mapped["Theme"] = relationship(back_populates="problems")
    created_by: Mapped["User"] = relationship(back_populates="created_problems")
    images: Mapped[list["ExplanationImage"]] = relationship(
        back_populates="problem",
        cascade="all, delete"
    )
    completed_by: Mapped[list["User"]] = relationship(
        back_populates="completed_problems",
        secondary="problem_user"
    )
    comments: Mapped["Comment"] = relationship(back_populates="problem")

    repr_cols = ("id", "name", "difficulty_level")


class ExplanationImage(Base):
    __tablename__ = "explanation_image"

    id: Mapped[intpk]
    image_url: Mapped[str]
    problem_id: Mapped[int | None] = mapped_column(
        ForeignKey("problem.id", ondelete="SET NULL"),
        nullable=True
    )

    problem: Mapped["Problem"] = relationship(back_populates="images")

    repr_cols = ("id", "problem_id")


class DoneProblem(Base):
    __tablename__ = "problem_user"

    problem_id: Mapped[int] = mapped_column(
        ForeignKey("problem.id", ondelete="CASCADE"),
        primary_key=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"),
        primary_key=True
    )


class Comment(Base):
    __tablename__ = "comment"

    id: Mapped[intpk]

    body: Mapped[str]
    likes: Mapped[int] = mapped_column(default=0)
    dislikes: Mapped[int] = mapped_column(default=0)
    author_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE")
    )
    problem_id: Mapped[int] = mapped_column(
        ForeignKey("problem.id", ondelete="CASCADE")
    )
    created_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow())

    created_by: Mapped["User"] = relationship(back_populates="comments")
    problem: Mapped["Problem"] = relationship(back_populates="comments")
    responses: Mapped[list["CommentResponse"]] = relationship(back_populates="comment")

    repr_cols = ("id", "created_at")


class CommentReaction(Base):
    __tablename__ = "comment_reaction"

    id: Mapped[intpk]
    comment_id: Mapped[int]
    user_id: Mapped[int]
    type: Mapped[enums.ReactionType]
    belongs_to: Mapped[enums.ReactionOwner] = mapped_column(nullable=True)

    repr_cols = ("id", "type")


class CommentResponse(Base):
    __tablename__ = "comment_response"

    id: Mapped[intpk]
    author_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE")
    )
    comment_id: Mapped[int] = mapped_column(
        ForeignKey("comment.id", ondelete="CASCADE")
    )
    body: Mapped[str]
    created_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow())

    created_by: Mapped["User"] = relationship(back_populates="comment_responses")
    comment: Mapped["Comment"] = relationship(back_populates="responses")
    likes: Mapped[int] = mapped_column(default=0)
    dislikes: Mapped[int] = mapped_column(default=0)

    repr_cols = ("id", "problem_id", "created_at")
