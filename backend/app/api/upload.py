from fastapi import APIRouter, UploadFile, File, Depends

from sqlalchemy.orm import Session

from app.services.ingestion import (
    validate_pdf,
    save_pdf
)

from app.core.database import get_db



router = APIRouter()



@router.post("/upload")
def upload_document(

    file: UploadFile = File(...),

    db: Session = Depends(get_db)

):


    validate_pdf(file)


    job = save_pdf(file)


    db.add(job)

    db.commit()

    db.refresh(job)


    return {

        "message": "PDF received successfully",

        "job_id": job.job_id,

        "filename": job.filename,

        "object_name": job.object_name,

        "status": job.status

    }