import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class InstitutionIn(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    university_name: str | None = Field(default=None, max_length=255)


class InstitutionOut(InstitutionIn):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID


class SubjectOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    name: str
    code: str | None


class ProjectBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    course: str | None = Field(default=None, max_length=255)
    semester: str | None = Field(default=None, max_length=50)
    exam_name: str | None = Field(default=None, max_length=255)
    duration_minutes: int | None = Field(default=None, gt=0, le=1440)
    max_marks: int | None = Field(default=None, gt=0, le=10000)
    description: str | None = Field(default=None, max_length=5000)
    exam_details: dict | None = None


class ProjectCreate(ProjectBase):
    institution: InstitutionIn | None = None
    subject_name: str | None = Field(default=None, min_length=1, max_length=255)
    subject_code: str | None = Field(default=None, max_length=50)


class ProjectUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    course: str | None = Field(default=None, max_length=255)
    semester: str | None = Field(default=None, max_length=50)
    exam_name: str | None = Field(default=None, max_length=255)
    duration_minutes: int | None = Field(default=None, gt=0, le=1440)
    max_marks: int | None = Field(default=None, gt=0, le=10000)
    description: str | None = Field(default=None, max_length=5000)
    exam_details: dict | None = None
    institution: InstitutionIn | None = None
    subject_name: str | None = Field(default=None, min_length=1, max_length=255)
    subject_code: str | None = Field(default=None, max_length=50)


class ProjectOut(ProjectBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    institution: InstitutionOut | None
    subject: SubjectOut | None
    created_at: datetime
    updated_at: datetime
