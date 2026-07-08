from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.models.job import Job

from app.services.analysis_service import analyze_job
from app.services.storage import download_pdf

import tempfile


router = APIRouter()


@router.post("/analyze/{job_id}")
def analyze_pdf(
    job_id: str,
    db: Session = Depends(get_db)
):

    # Recherche du job dans PostgreSQL
    job = db.query(Job).filter(
        Job.job_id == job_id
    ).first()


    if job is None:
        return {
            "error": "Job not found"
        }


    # Télécharger le PDF depuis MinIO
    pdf_bytes = download_pdf(
        job.object_name
    )


    # Création d'un fichier temporaire local
    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    )


    temp_file.write(pdf_bytes)

    temp_file.close()


    pdf_path = temp_file.name


    # Analyse Layer 1 : PDF Inspector
    pages = analyze_job(
        db,
        job,
        pdf_path
    )


    return {

        "job_id": job_id,

        "pages_analyzed": len(pages),

        "status": job.status

    }