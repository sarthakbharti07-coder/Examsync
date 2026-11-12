import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import SyllabusSource

# ---------- Syllabus ----------


class SyllabusCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    raw_text: str | None = None
    source: SyllabusSource = SyllabusSource.MANUAL


class SyllabusUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    raw_text: str | None = None


class SyllabusOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    project_id: uuid.UUID
    document_id: uuid.UUID | None
    source: SyllabusSource
    title: str | None
    raw_text: str | None
    coverage_report: dict | None
    created_at: datetime
    updated_at: datetime


# ---------- Units ----------


class UnitCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    position: int = Field(default=0, ge=0)


class UnitUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    position: int | None = Field(default=None, ge=0)


class UnitOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    syllabus_id: uuid.UUID
    name: str
    position: int
    created_at: datetime
    updated_at: datetime


# ---------- Topics ----------


class TopicCreate(BaseModel):
    name: str = Field(min_length=1, max_length=500)
    position: int = Field(default=0, ge=0)
    parent_topic_id: uuid.UUID | None = None


class TopicUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=500)
    position: int | None = Field(default=None, ge=0)


class TopicOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    unit_id: uuid.UUID
    parent_topic_id: uuid.UUID | None
    name: str
    position: int
    created_at: datetime
    updated_at: datetime
