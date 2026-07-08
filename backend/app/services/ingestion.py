import uuid

from fastapi import UploadFile, HTTPException

from app.models.job import Job

from app.services.storage import upload_pdf



MAX_FILE_SIZE = 50 * 1024 * 1024



def validate_pdf(file: UploadFile):

    if not file.filename.lower().endswith(".pdf"):

        raise HTTPException(
            status_code=400,
            detail="File must be PDF"
        )



def save_pdf(file: UploadFile):


    job_id = str(uuid.uuid4())


    content = file.file.read()



    if len(content) > MAX_FILE_SIZE:

        raise HTTPException(
            status_code=400,
            detail="File too large"
        )



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