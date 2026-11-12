import uuid

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import ExaminationProject, Institution, Subject, User
from app.schemas.project import InstitutionIn


def _get_or_create_institution(db: Session, owner: User, data: InstitutionIn) -> Institution:
    inst = db.scalar(
        select(Institution).where(
            Institution.owner_id == owner.id,
            Institution.name == data.name,
            Institution.university_name.is_(data.university_name)
            if data.university_name is None
            else Institution.university_name == data.university_name,
        )
    )
    if inst is None:
        inst = Institution(owner_id=owner.id, name=data.name, university_name=data.university_name)
        db.add(inst)
        db.flush()
    return inst


def _get_or_create_subject(db: Session, owner: User, name: str, code: str | None) -> Subject:
    subj = db.scalar(select(Subject).where(Subject.owner_id == owner.id, Subject.name == name))
    if subj is None:
        subj = Subject(owner_id=owner.id, name=name, code=code)
        db.add(subj)
        db.flush()
    elif code and not subj.code:
        subj.code = code
    return subj


def create(db: Session, owner: User, data: dict) -> ExaminationProject:
    institution = data.pop("institution", None)
    subject_name = data.pop("subject_name", None)
    subject_code = data.pop("subject_code", None)
    project = ExaminationProject(owner_id=owner.id, **data)
    if institution:
        project.institution = _get_or_create_institution(db, owner, InstitutionIn(**institution))
    if subject_name:
        project.subject = _get_or_create_subject(db, owner, subject_name, subject_code)
    db.add(project)
    db.commit()
    return project


def get_owned(db: Session, owner: User, project_id: uuid.UUID) -> ExaminationProject | None:
    """Returns None for both 'missing' and 'someone else's' so callers can 404 either way."""
    return db.scalar(
        select(ExaminationProject).where(
            ExaminationProject.id == project_id, ExaminationProject.owner_id == owner.id
        )
    )


def list_owned(db: Session, owner: User, limit: int, offset: int) -> tuple[list[ExaminationProject], int]:
    base = select(ExaminationProject).where(ExaminationProject.owner_id == owner.id)
    total = db.scalar(select(func.count()).select_from(base.subquery())) or 0
    items = db.scalars(base.order_by(ExaminationProject.created_at.desc(), ExaminationProject.id).limit(limit).offset(offset)).unique().all()
    return list(items), total


def update(db: Session, owner: User, project: ExaminationProject, data: dict) -> ExaminationProject:
    institution = data.pop("institution", None)
    subject_name = data.pop("subject_name", None)
    subject_code = data.pop("subject_code", None)
    for key, value in data.items():
        setattr(project, key, value)
    if institution:
        project.institution = _get_or_create_institution(db, owner, InstitutionIn(**institution))
    if subject_name:
        project.subject = _get_or_create_subject(db, owner, subject_name, subject_code)
    db.commit()
    return project


def delete(db: Session, project: ExaminationProject) -> None:
    db.delete(project)
    db.commit()
