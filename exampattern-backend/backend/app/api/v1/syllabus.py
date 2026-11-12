
import uuid

from fastapi import APIRouter, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import CurrentUser, DbSession
from app.models.project import ExaminationProject
from app.models.syllabus import Syllabus, SyllabusUnit, SyllabusTopic
from app.schemas.syllabus import (
    SyllabusCreate,
    SyllabusUpdate,
    SyllabusOut,
    UnitCreate,
    UnitUpdate,
    UnitOut,
    TopicCreate,
    TopicUpdate,
    TopicOut,
)

router = APIRouter(prefix="/syllabus", tags=["syllabus"])


# ---------- Ownership helpers ----------

def get_owned_project(db: Session, user, project_id: uuid.UUID):
    project = db.scalar(
        select(ExaminationProject).where(
            ExaminationProject.id == project_id,
            ExaminationProject.owner_id == user.id,
        )
    )

    if project is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "Project not found",
        )

    return project


def get_owned_syllabus(db: Session, user, syllabus_id: uuid.UUID):
    syllabus = db.scalar(
        select(Syllabus)
        .join(
            ExaminationProject,
            Syllabus.project_id == ExaminationProject.id,
        )
        .where(
            Syllabus.id == syllabus_id,
            ExaminationProject.owner_id == user.id,
        )
    )

    if syllabus is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "Syllabus not found",
        )

    return syllabus


def get_owned_unit(db: Session, user, unit_id: uuid.UUID):
    unit = db.scalar(
        select(SyllabusUnit)
        .join(
            Syllabus,
            SyllabusUnit.syllabus_id == Syllabus.id,
        )
        .join(
            ExaminationProject,
            Syllabus.project_id == ExaminationProject.id,
        )
        .where(
            SyllabusUnit.id == unit_id,
            ExaminationProject.owner_id == user.id,
        )
    )

    if unit is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "Unit not found",
        )

    return unit


def get_owned_topic(db: Session, user, topic_id: uuid.UUID):
    topic = db.scalar(
        select(SyllabusTopic)
        .join(
            SyllabusUnit,
            SyllabusTopic.unit_id == SyllabusUnit.id,
        )
        .join(
            Syllabus,
            SyllabusUnit.syllabus_id == Syllabus.id,
        )
        .join(
            ExaminationProject,
            Syllabus.project_id == ExaminationProject.id,
        )
        .where(
            SyllabusTopic.id == topic_id,
            ExaminationProject.owner_id == user.id,
        )
    )

    if topic is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "Topic not found",
        )

    return topic


# ---------- Syllabus endpoints ----------

@router.post(
    "/project/{project_id}",
    response_model=SyllabusOut,
    status_code=status.HTTP_201_CREATED,
)
def create_syllabus(
    project_id: uuid.UUID,
    body: SyllabusCreate,
    db: DbSession,
    user: CurrentUser,
):
    get_owned_project(db, user, project_id)

    syllabus = Syllabus(
        project_id=project_id,
        title=body.title,
        raw_text=body.raw_text,
        source=body.source,
    )

    db.add(syllabus)
    db.commit()
    db.refresh(syllabus)

    return syllabus


@router.get(
    "/project/{project_id}",
    response_model=list[SyllabusOut],
)
def list_syllabuses(
    project_id: uuid.UUID,
    db: DbSession,
    user: CurrentUser,
):
    get_owned_project(db, user, project_id)

    return db.scalars(
        select(Syllabus)
        .where(Syllabus.project_id == project_id)
        .order_by(Syllabus.created_at.desc())
    ).all()


@router.get(
    "/{syllabus_id}",
    response_model=SyllabusOut,
)
def get_syllabus(
    syllabus_id: uuid.UUID,
    db: DbSession,
    user: CurrentUser,
):
    return get_owned_syllabus(db, user, syllabus_id)


@router.patch(
    "/{syllabus_id}",
    response_model=SyllabusOut,
)
def update_syllabus(
    syllabus_id: uuid.UUID,
    body: SyllabusUpdate,
    db: DbSession,
    user: CurrentUser,
):
    syllabus = get_owned_syllabus(db, user, syllabus_id)

    for key, value in body.model_dump(exclude_unset=True).items():
        setattr(syllabus, key, value)

    db.commit()
    db.refresh(syllabus)

    return syllabus


@router.delete(
    "/{syllabus_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_syllabus(
    syllabus_id: uuid.UUID,
    db: DbSession,
    user: CurrentUser,
):
    syllabus = get_owned_syllabus(db, user, syllabus_id)

    db.delete(syllabus)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# ---------- Unit endpoints ----------

@router.post(
    "/{syllabus_id}/units",
    response_model=UnitOut,
    status_code=status.HTTP_201_CREATED,
)
def create_unit(
    syllabus_id: uuid.UUID,
    body: UnitCreate,
    db: DbSession,
    user: CurrentUser,
):
    syllabus = get_owned_syllabus(db, user, syllabus_id)

    unit = SyllabusUnit(
        syllabus_id=syllabus.id,
        name=body.name,
        position=body.position,
    )

    db.add(unit)
    db.commit()
    db.refresh(unit)

    return unit


@router.get(
    "/{syllabus_id}/units",
    response_model=list[UnitOut],
)
def list_units(
    syllabus_id: uuid.UUID,
    db: DbSession,
    user: CurrentUser,
):
    syllabus = get_owned_syllabus(db, user, syllabus_id)

    return db.scalars(
        select(SyllabusUnit)
        .where(SyllabusUnit.syllabus_id == syllabus.id)
        .order_by(
            SyllabusUnit.position,
            SyllabusUnit.created_at,
        )
    ).all()


@router.patch(
    "/units/{unit_id}",
    response_model=UnitOut,
)
def update_unit(
    unit_id: uuid.UUID,
    body: UnitUpdate,
    db: DbSession,
    user: CurrentUser,
):
    unit = get_owned_unit(db, user, unit_id)

    for key, value in body.model_dump(exclude_unset=True).items():
        setattr(unit, key, value)

    db.commit()
    db.refresh(unit)

    return unit


@router.delete(
    "/units/{unit_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_unit(
    unit_id: uuid.UUID,
    db: DbSession,
    user: CurrentUser,
):
    unit = get_owned_unit(db, user, unit_id)

    db.delete(unit)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# ---------- Topic endpoints ----------

@router.post(
    "/units/{unit_id}/topics",
    response_model=TopicOut,
    status_code=status.HTTP_201_CREATED,
)
def create_topic(
    unit_id: uuid.UUID,
    body: TopicCreate,
    db: DbSession,
    user: CurrentUser,
):
    unit = get_owned_unit(db, user, unit_id)

    if body.parent_topic_id:
        parent = get_owned_topic(
            db,
            user,
            body.parent_topic_id,
        )

        if parent.unit_id != unit.id:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "Parent topic must belong to the same unit",
            )

    topic = SyllabusTopic(
        unit_id=unit.id,
        name=body.name,
        position=body.position,
        parent_topic_id=body.parent_topic_id,
    )

    db.add(topic)
    db.commit()
    db.refresh(topic)

    return topic


@router.get(
    "/units/{unit_id}/topics",
    response_model=list[TopicOut],
)
def list_topics(
    unit_id: uuid.UUID,
    db: DbSession,
    user: CurrentUser,
):
    unit = get_owned_unit(db, user, unit_id)

    return db.scalars(
        select(SyllabusTopic)
        .where(SyllabusTopic.unit_id == unit.id)
        .order_by(
            SyllabusTopic.position,
            SyllabusTopic.created_at,
        )
    ).all()


@router.patch(
    "/topics/{topic_id}",
    response_model=TopicOut,
)
def update_topic(
    topic_id: uuid.UUID,
    body: TopicUpdate,
    db: DbSession,
    user: CurrentUser,
):
    topic = get_owned_topic(db, user, topic_id)

    for key, value in body.model_dump(exclude_unset=True).items():
        setattr(topic, key, value)

    db.commit()
    db.refresh(topic)

    return topic


@router.delete(
    "/topics/{topic_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_topic(
    topic_id: uuid.UUID,
    db: DbSession,
    user: CurrentUser,
):
    topic = get_owned_topic(db, user, topic_id)

    db.delete(topic)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
