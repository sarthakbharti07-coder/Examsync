import uuid
from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, Index, Integer, String, Text, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, Timestamps, UUIDPrimaryKey, str_enum
from app.models.enums import DocumentKind, DocumentStatus


class UploadedDocument(UUIDPrimaryKey, Timestamps, Base):
    __tablename__ = "uploaded_documents"
    __table_args__ = (
        UniqueConstraint("project_id", "sha256", name="uq_document_project_sha256"),  # duplicate prevention
        Index("ix_documents_project_status", "project_id", "status"),
    )

    project_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("examination_projects.id", ondelete="CASCADE"), index=True
    )
    owner_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("users.id", ondelete="CASCADE"), index=True)

    kind: Mapped[DocumentKind] = mapped_column(str_enum(DocumentKind), default=DocumentKind.QUESTION_PAPER)
    original_filename: Mapped[str] = mapped_column(String(255))
    content_type: Mapped[str] = mapped_column(String(100))
    file_size: Mapped[int] = mapped_column(BigInteger)
    sha256: Mapped[str] = mapped_column(String(64))
    storage_key: Mapped[str] = mapped_column(String(500))
    page_count: Mapped[int | None] = mapped_column(Integer)
    exam_label: Mapped[str | None] = mapped_column(String(100))  # e.g. "2023 End Sem"
    exam_year: Mapped[int | None] = mapped_column(Integer)

    status: Mapped[DocumentStatus] = mapped_column(str_enum(DocumentStatus), default=DocumentStatus.UPLOADED)
    error_message: Mapped[str | None] = mapped_column(Text)
    task_id: Mapped[str | None] = mapped_column(String(100))
    extraction_method: Mapped[str | None] = mapped_column(String(50))  # text | ocr | multimodal
    processed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
