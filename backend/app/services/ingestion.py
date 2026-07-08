import uuid
from fastapi import UploadFile, HTTPException

from app.models.job import Job
from app.services.storage import upload_pdf


MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB


def validate_pdf(file: UploadFile):

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="File must be PDF"
        )


def save_pdf(file: UploadFile, db):

    # Génération ID
    job_id = uuid.uuid4()

    filename = file.filename

    object_name = f"{job_id}.pdf"


    # Lecture fichier
    content = file.file.read()


    # Vérification taille
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File too large"
        )


    # Upload vers MinIO
    upload_pdf(
        object_name,
        content
    )


    # Création du job PostgreSQL
    job = Job(
        job_id=job_id,
        filename=filename,
        object_name=object_name,
        status="RECEIVED"
    )


    # Sauvegarde DB
    db.add(job)
    db.commit()
    db.refresh(job)


    return job