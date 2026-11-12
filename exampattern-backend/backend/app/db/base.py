import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum as SAEnum, Uuid, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class UUIDPrimaryKey:
    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)


class Timestamps:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


def str_enum(enum_cls: type[enum.Enum]) -> SAEnum:
    """Store enums as plain VARCHAR holding the enum *value* (portable, easy to migrate)."""
    return SAEnum(
        enum_cls,
        native_enum=False,
        length=32,
        values_callable=lambda e: [m.value for m in e],
        validate_strings=True,
    )
