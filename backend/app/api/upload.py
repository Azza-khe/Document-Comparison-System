from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db

from app.services.ingestion import (
    validate_pdf,
    save_pdf
)




router = APIRouter()


@router.post("/upload")
def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    # Validation du fichier PDF
    validate_pdf(file)

    # Upload MinIO + insertion PostgreSQL
    job = save_pdf(file, db)


    return {

        "message": "PDF received successfully",

        "job_id": str(job.job_id),

        "status": job.status

    }