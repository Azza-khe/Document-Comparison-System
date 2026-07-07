import os
import uuid
from fastapi import UploadFile, HTTPException

from app.models.job import Job
from app.services.storage import upload_pdf


UPLOAD_FOLDER = "storage/uploads"

MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB


def validate_pdf(file: UploadFile):

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="File must be PDF"
        )


def save_pdf(file: UploadFile):

    job_id = uuid.uuid4()

    filename = f"{job_id}.pdf"

    content = file.file.read()

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File too large"
        )

    path = upload_pdf(
        filename,
        content
    )

    return Job(
        job_id=job_id,
        filename=filename
    )