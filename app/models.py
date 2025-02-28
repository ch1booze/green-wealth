import uuid

from sqlalchemy.orm import Mapped, mapped_column

from app import db


class User(db.Model):
    id: Mapped[str] = mapped_column(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True,
    )
    email: Mapped[str] = mapped_column(unique=True)
    full_name: Mapped[str]
