import uuid

from sqlalchemy import ForeignKey, Integer, JSON, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, Timestamps, UUIDPrimaryKey, str_enum
from app.models.enums import AnalysisStatus


class PatternAnalysis(UUIDPrimaryKey, Timestamps, Base):
    __tablename__ = "pattern_analyses"

    project_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("examination_projects.id", ondelete="CASCADE"), index=True
    )
    status: Mapped[AnalysisStatus] = mapped_column(str_enum(AnalysisStatus), default=AnalysisStatus.PENDING)
    paper_count: Mapped[int] = mapped_column(Integer, default=0)  # sample size is always recorded
    question_count: Mapped[int] = mapped_column(Integer, default=0)
    metrics: Mapped[dict | None] = mapped_column(JSON)  # computed in Python
    ai_interpretation: Mapped[dict | None] = mapped_column(JSON)  # semantic findings from the LLM
    task_id: Mapped[str | None] = mapped_column(Text)
    error_message: Mapped[str | None] = mapped_column(Text)
