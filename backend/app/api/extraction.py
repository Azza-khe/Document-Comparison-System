from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.models.extracted_document import ExtractedDocument
from app.models.document_group import DocumentGroup


router = APIRouter(
    prefix="/api/extraction",
    tags=["Extraction"]
)



@router.get("/{job_id}")
def get_extractions(
    job_id: str,
    db: Session = Depends(get_db)
):


    results = (
        db.query(ExtractedDocument)
        .join(
            DocumentGroup,
            ExtractedDocument.document_group_id 
            == DocumentGroup.id
        )
        .filter(
            DocumentGroup.job_id == job_id
        )
        .all()
    )


    if not results:

        raise HTTPException(
            status_code=404,
            detail="No extracted documents found"
        )


    response = []


    for document in results:

        response.append({

            "id": document.id,

            "document_group_id":
                document.document_group_id,

            "doc_type":
                document.doc_type,

            "data":
                document.extracted_data,

            "confidence":
                document.confidence,

            "source":
                document.extraction_source,

            "created_at":
                document.created_at

        })


    return response