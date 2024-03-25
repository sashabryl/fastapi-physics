from sqlalchemy.orm import mapped_column, Mapped

from database import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    email: Mapped[str]
    score: Mapped[int] = mapped_column(default=0)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    hash_password: Mapped[bytes]

    repr_cols = ("id", "username", "email", "is_superuser")
