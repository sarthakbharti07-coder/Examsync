import uuid

from sqlalchemy import Boolean, ForeignKey, Index, Integer, JSON, Numeric, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, Timestamps, UUIDPrimaryKey, str_enum
from app.models.enums import PaperStatus


class GeneratedPaper(UUIDPrimaryKey, Timestamps, Base):
    __tablename__ = "generated_papers"

    project_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("examination_projects.id", ondelete="CASCADE"), index=True
    )
    owner_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    syllabus_id: Mapped[uuid.UUID | None] = mapped_column(Uuid, ForeignKey("syllabus.id", ondelete="SET NULL"))
    analysis_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("pattern_analyses.id", ondelete="SET NULL")
    )

    status: Mapped[PaperStatus] = mapped_column(str_enum(PaperStatus), default=PaperStatus.GENERATING)
    config: Mapped[dict] = mapped_column(JSON)  # the student's generation request
    structure: Mapped[dict | None] = mapped_column(JSON)  # section layout + instructions
    total_marks: Mapped[float | None] = mapped_column(Numeric(7, 2))
    duration_minutes: Mapped[int | None] = mapped_column(Integer)
    pdf_storage_key: Mapped[str | None] = mapped_column(String(500))
    task_id: Mapped[str | None] = mapped_column(String(100))
    error_message: Mapped[str | None] = mapped_column(Text)


class GeneratedQuestion(UUIDPrimaryKey, Timestamps, Base):
    """AI-generated questions: kept strictly separate from historical extracted_questions."""

    __tablename__ = "generated_questions"
    __table_args__ = (Index("ix_genq_paper_position", "paper_id", "position"),)

    paper_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("generated_papers.id", ondelete="CASCADE"), index=True)
    position: Mapped[int] = mapped_column(Integer, default=0)
    section: Mapped[str | None] = mapped_column(String(100))
    question_number: Mapped[str] = mapped_column(String(50))
    question_text: Mapped[str] = mapped_column(Text)
    marks: Mapped[float] = mapped_column(Numeric(6, 2))
    question_type: Mapped[str | None] = mapped_column(String(50))
    difficulty: Mapped[str | None] = mapped_column(String(20))
    unit: Mapped[str | None] = mapped_column(String(255))
    topic: Mapped[str | None] = mapped_column(String(255))
    has_programming: Mapped[bool] = mapped_column(Boolean, default=False)
    choice_group: Mapped[str | None] = mapped_column(String(50))  # questions sharing a group are "attempt one of"
    is_edited: Mapped[bool] = mapped_column(Boolean, default=False)


class PaperVerification(UUIDPrimaryKey, Timestamps, Base):
    __tablename__ = "paper_verifications"

    paper_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("generated_papers.id", ondelete="CASCADE"), index=True)
    passed: Mapped[bool] = mapped_column(Boolean)
    numeric_checks: Mapped[dict | None] = mapped_column(JSON)  # Python validation results
    ai_findings: Mapped[dict | None] = mapped_column(JSON)  # semantic checks from the LLM
    warnings: Mapped[list | None] = mapped_column(JSON)
    regenerated_question_ids: Mapped[list | None] = mapped_column(JSON)
