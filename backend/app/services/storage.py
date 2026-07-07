from minio import Minio
from io import BytesIO


client = Minio(
    "localhost:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False
)


BUCKET_NAME = "documents"


def upload_pdf(
    filename: str,
    file_bytes: bytes
):

    client.put_object(
        bucket_name=BUCKET_NAME,
        object_name=filename,
        data=BytesIO(file_bytes),
        length=len(file_bytes),
        content_type="application/pdf"
    )


    return f"{BUCKET_NAME}/{filename}"