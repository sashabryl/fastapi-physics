from sqlalchemy.orm import mapped_column, Mapped, relationship

from database import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    score: Mapped[int] = mapped_column(default=0)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    hash_password: Mapped[bytes]

    completed_problems: Mapped[list["Problem"]] = relationship(
        back_populates="completed_by",
        secondary="problem_user"
    )

    created_problems: Mapped[list["Problem"]] = relationship(
        back_populates="created_by"
    )
    comments: Mapped[list["Comment"]] = relationship(
        back_populates="created_by"
    )

    repr_cols = ("id", "username", "email", "is_superuser")
