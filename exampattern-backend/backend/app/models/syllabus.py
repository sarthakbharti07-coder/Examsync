import uuid

from sqlalchemy import ForeignKey, Integer, JSON, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, Timestamps, UUIDPrimaryKey, str_enum
from app.models.enums import SyllabusSource


class Syllabus(UUIDPrimaryKey, Timestamps, Base):
    __tablename__ = "syllabus"

    project_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("examination_projects.id", ondelete="CASCADE"), index=True
    )
    document_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("uploaded_documents.id", ondelete="SET NULL")
    )
    source: Mapped[SyllabusSource] = mapped_column(str_enum(SyllabusSource))
    title: Mapped[str | None] = mapped_column(String(255))
    raw_text: Mapped[str | None] = mapped_column(Text)
    coverage_report: Mapped[dict | None] = mapped_column(JSON)


class SyllabusUnit(UUIDPrimaryKey, Timestamps, Base):
    __tablename__ = "syllabus_units"

    syllabus_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("syllabus.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String(255))
    position: Mapped[int] = mapped_column(Integer, default=0)


class SyllabusTopic(UUIDPrimaryKey, Timestamps, Base):
    __tablename__ = "syllabus_topics"

    unit_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("syllabus_units.id", ondelete="CASCADE"), index=True)
    parent_topic_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("syllabus_topics.id", ondelete="CASCADE")
    )  # set for subtopics
    name: Mapped[str] = mapped_column(String(500))
    position: Mapped[int] = mapped_column(Integer, default=0)
