import uuid

from sqlalchemy import Boolean, ForeignKey, String, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, Timestamps, UUIDPrimaryKey


class User(UUIDPrimaryKey, Timestamps, Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(320), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    full_name: Mapped[str | None] = mapped_column(String(200))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class Institution(UUIDPrimaryKey, Timestamps, Base):
    """A college/university profile owned by one student (no institution formats are hardcoded)."""

    __tablename__ = "institutions"
    __table_args__ = (UniqueConstraint("owner_id", "name", "university_name", name="uq_institution_owner_name"),)

    owner_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String(255))
    university_name: Mapped[str | None] = mapped_column(String(255))
