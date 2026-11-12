import hashlib
import uuid
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.api.deps import CurrentUser, DbSession
from app.core.config import settings
from app.models.document import UploadedDocument
from app.models.project import ExaminationProject
from app.services.storage import upload_file, delete_file

router = APIRouter(prefix="/documents", tags=["documents"])

CHUNK_SIZE = 1024 * 1024


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_document(
    project_id: uuid.UUID,
    db: DbSession,
    user: CurrentUser,
    file: UploadFile = File(...),
):
    try:
        # 1. Verify project ownership
        project = db.scalar(
            select(ExaminationProject).where(
                ExaminationProject.id == project_id,
                ExaminationProject.owner_id == user.id,
            )
        )

        if project is None:
            raise HTTPException(
                status_code=404,
                detail="Project not found",
            )

        # 2. Validate filename
        filename = Path((file.filename or "").replace("\\", "/")).name

        if not filename or not filename.lower().endswith(".pdf"):
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are allowed",
            )

        if file.content_type not in (
            "application/pdf",
            "application/octet-stream",
        ):
            raise HTTPException(
                status_code=400,
                detail="Invalid content type",
            )

        # 3. Read file with size limit and calculate SHA-256
        max_file_size = settings.max_upload_mb * 1024 * 1024

        content = bytearray()
        digest = hashlib.sha256()

        while chunk := await file.read(CHUNK_SIZE):
            if len(content) + len(chunk) > max_file_size:
                raise HTTPException(
                    status_code=413,
                    detail=f"PDF exceeds {settings.max_upload_mb} MB limit",
                )

            content.extend(chunk)
            digest.update(chunk)

        if not content.startswith(b"%PDF-"):
            raise HTTPException(
                status_code=400,
                detail="Invalid PDF file",
            )

        if not content:
            raise HTTPException(
                status_code=400,
                detail="The uploaded file is empty",
            )

        sha256 = digest.hexdigest()

        # 4. Prevent duplicate uploads
        existing = db.scalar(
            select(UploadedDocument).where(
                UploadedDocument.project_id == project_id,
                UploadedDocument.sha256 == sha256,
            )
        )

        if existing:
            raise HTTPException(
                status_code=409,
                detail="This PDF is already uploaded to this project",
            )

        # 5. Generate a unique storage path
        storage_key = f"{project_id}/{uuid.uuid4()}.pdf"

        # 6. Upload PDF to Supabase Storage
        try:
            upload_file(storage_key, bytes(content))
        except Exception as exc:
            raise HTTPException(
                status_code=502,
                detail="Could not upload PDF to cloud storage",
            ) from exc

        # 7. Save document metadata in PostgreSQL
        document = UploadedDocument(
            project_id=project_id,
            owner_id=user.id,
            original_filename=filename,
            content_type="application/pdf",
            file_size=len(content),
            sha256=sha256,
            storage_key=storage_key,
        )

        try:
            db.add(document)
            db.commit()
            db.refresh(document)

        except IntegrityError as exc:
            db.rollback()
            try:
                delete_file(storage_key)
            except Exception:
                pass

            raise HTTPException(
                status_code=409,
                detail="This PDF is already uploaded to this project",
            ) from exc

        except Exception as exc:
            db.rollback()

            try:
                delete_file(storage_key)
            except Exception:
                pass

            raise HTTPException(
                status_code=500,
                detail="Could not save document information",
            ) from exc

        # 8. Return upload information
        return {
            "id": str(document.id),
            "project_id": str(document.project_id),
            "filename": document.original_filename,
            "file_size": document.file_size,
            "status": document.status.value,
            "message": "PDF uploaded successfully",
        }

    finally:
        await file.close()
