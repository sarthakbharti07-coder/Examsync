import uuid
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, Response, status

from app.api.deps import CurrentUser, DbSession
from app.repositories import projects as repo
from app.schemas.common import Page
from app.schemas.project import ProjectCreate, ProjectOut, ProjectUpdate

router = APIRouter(prefix="/projects", tags=["projects"])


def _owned_or_404(db, user, project_id: uuid.UUID):
    project = repo.get_owned(db, user, project_id)
    if project is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Project not found")
    return project


@router.post("", response_model=ProjectOut, status_code=status.HTTP_201_CREATED)
def create_project(body: ProjectCreate, db: DbSession, user: CurrentUser):
    return repo.create(db, user, body.model_dump())


@router.get("", response_model=Page[ProjectOut])
def list_projects(
    db: DbSession,
    user: CurrentUser,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
):
    items, total = repo.list_owned(db, user, limit, offset)
    return Page[ProjectOut](items=items, total=total, limit=limit, offset=offset)


@router.get("/{project_id}", response_model=ProjectOut)
def get_project(project_id: uuid.UUID, db: DbSession, user: CurrentUser):
    return _owned_or_404(db, user, project_id)


@router.patch("/{project_id}", response_model=ProjectOut)
def update_project(project_id: uuid.UUID, body: ProjectUpdate, db: DbSession, user: CurrentUser):
    project = _owned_or_404(db, user, project_id)
    return repo.update(db, user, project, body.model_dump(exclude_unset=True))


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: uuid.UUID, db: DbSession, user: CurrentUser):
    repo.delete(db, _owned_or_404(db, user, project_id))
    return Response(status_code=status.HTTP_204_NO_CONTENT)
