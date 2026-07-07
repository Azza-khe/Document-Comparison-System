from fastapi import APIRouter, UploadFile, File

from app.services.ingestion import (
    validate_pdf,
    save_pdf
)


router = APIRouter()


@router.post("/upload")
def upload_document(
    file: UploadFile = File(...)
):

    validate_pdf(file)

    job = save_pdf(file)


    return {

        "message": "PDF received successfully",

        "job_id": str(job.job_id),

        "status": job.status

    }