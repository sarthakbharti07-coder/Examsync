import uuid

from sqlalchemy import Boolean, Float, ForeignKey, Index, Integer, JSON, Numeric, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, Timestamps, UUIDPrimaryKey, str_enum
from app.models.enums import ClassificationSource


class ExtractedQuestion(UUIDPrimaryKey, Timestamps, Base):
    """Historical question exactly as extracted. Never overwritten by user corrections
    (corrections live in question_classifications)."""

    __tablename__ = "extracted_questions"
    __table_args__ = (Index("ix_extracted_project_doc", "project_id", "document_id"),)

    project_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("examination_projects.id", ondelete="CASCADE"), index=True
    )
    document_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("uploaded_documents.id", ondelete="CASCADE"), index=True
    )
    parent_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("extracted_questions.id", ondelete="CASCADE"), index=True
    )  # set for subquestions

    position: Mapped[int] = mapped_column(Integer, default=0)
    question_number: Mapped[str | None] = mapped_column(String(50))
    question_text: Mapped[str] = mapped_column(Text)
    marks: Mapped[float | None] = mapped_column(Numeric(6, 2))  # NULL = not identifiable; never invented
    section: Mapped[str | None] = mapped_column(String(100))
    question_type: Mapped[str | None] = mapped_column(String(50))
    subject: Mapped[str | None] = mapped_column(String(255))
    unit: Mapped[str | None] = mapped_column(String(255))
    topic: Mapped[str | None] = mapped_column(String(255))  # "unknown" when not confident
    page_number: Mapped[int | None] = mapped_column(Integer)
    confidence: Mapped[float | None] = mapped_column(Float)
    has_programming: Mapped[bool] = mapped_column(Boolean, default=False)
    extraction_warnings: Mapped[list | None] = mapped_column(JSON)  # nothing is silently discarded


class QuestionClassification(UUIDPrimaryKey, Timestamps, Base):
    __tablename__ = "question_classifications"
    __table_args__ = (Index("ix_classification_question_current", "question_id", "is_current"),)

    question_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("extracted_questions.id", ondelete="CASCADE"), index=True
    )
    source: Mapped[ClassificationSource] = mapped_column(str_enum(ClassificationSource))
    is_current: Mapped[bool] = mapped_column(Boolean, default=True)

    subject: Mapped[str | None] = mapped_column(String(255))
    unit: Mapped[str | None] = mapped_column(String(255))
    topic: Mapped[str | None] = mapped_column(String(255))
    subtopic: Mapped[str | None] = mapped_column(String(255))
    marks: Mapped[float | None] = mapped_column(Numeric(6, 2))
    difficulty: Mapped[str | None] = mapped_column(String(20))  # easy | moderate | difficult
    question_type: Mapped[str | None] = mapped_column(String(50))
    category: Mapped[str | None] = mapped_column(String(30))  # theory | programming | numerical
    cognitive_level: Mapped[str | None] = mapped_column(String(50))
    confidence: Mapped[float | None] = mapped_column(Float)
