import uuid

import fitz

from fastapi import UploadFile, HTTPException

from app.models.job import Job

from app.services.storage import upload_pdf



MAX_FILE_SIZE = 50 * 1024 * 1024



# =====================================================
# PDF Validation
# =====================================================

def validate_pdf(file: UploadFile):


    # -----------------------------
    # Vérification extension
    # -----------------------------

    if not file.filename.lower().endswith(".pdf"):

        raise HTTPException(

            status_code=400,

            detail="File must be PDF"

        )


    # -----------------------------
    # Lire contenu temporairement
    # -----------------------------

    content = file.file.read()


    if len(content) == 0:

        raise HTTPException(

            status_code=400,

            detail="Empty file"

        )


    # Replacer curseur fichier
    file.file.seek(0)



    # -----------------------------
    # Taille maximale
    # -----------------------------

    if len(content) > MAX_FILE_SIZE:

        raise HTTPException(

            status_code=400,

            detail="File too large (max 50MB)"

        )



    # -----------------------------
    # Vérification vrai PDF
    # -----------------------------

    try:

        pdf = fitz.open(

            stream=content,

            filetype="pdf"

        )


    except Exception:

        raise HTTPException(

            status_code=400,

            detail="Corrupted PDF"

        )



    # -----------------------------
    # PDF protégé
    # -----------------------------

    if pdf.needs_pass:

        pdf.close()

        raise HTTPException(

            status_code=400,

            detail="Password protected PDF"

        )



    # -----------------------------
    # Nombre de pages
    # -----------------------------

    if pdf.page_count == 0:

        pdf.close()

        raise HTTPException(

            status_code=400,

            detail="PDF contains no pages"

        )


    pdf.close()



    return True






# =====================================================
# Save PDF to MinIO + Create Job
# =====================================================

def save_pdf(file: UploadFile):


    job_id = str(uuid.uuid4())


    content = file.file.read()



    object_name = upload_pdf(

        job_id,

        content

    )



    return Job(

        job_id=job_id,

        filename=file.filename,

        object_name=object_name,

        status="RECEIVED"

    )