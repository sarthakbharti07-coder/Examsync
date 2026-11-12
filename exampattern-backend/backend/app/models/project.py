import uuid

from sqlalchemy import ForeignKey, Integer, JSON, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, Timestamps, UUIDPrimaryKey


class Subject(UUIDPrimaryKey, Timestamps, Base):
    __tablename__ = "subjects"

    owner_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String(255))
    code: Mapped[str | None] = mapped_column(String(50))


class ExaminationProject(UUIDPrimaryKey, Timestamps, Base):
    __tablename__ = "examination_projects"

    owner_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    institution_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("institutions.id", ondelete="SET NULL"), index=True
    )
    subject_id: Mapped[uuid.UUID | None] = mapped_column(Uuid, ForeignKey("subjects.id", ondelete="SET NULL"))

    title: Mapped[str] = mapped_column(String(255))
    course: Mapped[str | None] = mapped_column(String(255))
    semester: Mapped[str | None] = mapped_column(String(50))
    exam_name: Mapped[str | None] = mapped_column(String(255))  # e.g. "End Semester", "Mid Term"
    duration_minutes: Mapped[int | None] = mapped_column(Integer)
    max_marks: Mapped[int | None] = mapped_column(Integer)
    description: Mapped[str | None] = mapped_column(Text)
    exam_details: Mapped[dict | None] = mapped_column(JSON)  # free-form extras

    institution: Mapped["Institution | None"] = relationship(lazy="joined")  # noqa: F821
    subject: Mapped["Subject | None"] = relationship(lazy="joined")
