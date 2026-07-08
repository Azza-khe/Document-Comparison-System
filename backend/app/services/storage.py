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
    job_id: str,
    file_bytes: bytes
):

    # Structure :
    # documents/pdfs/job_id.pdf

    object_name = (
        f"pdfs/{job_id}.pdf"
    )


    client.put_object(

        bucket_name=BUCKET_NAME,

        object_name=object_name,

        data=BytesIO(file_bytes),

        length=len(file_bytes),

        content_type="application/pdf"

    )


    return object_name



def download_pdf(object_name):

    response = client.get_object(
        BUCKET_NAME,
        object_name
    )


    data = response.read()


    response.close()
    response.release_conn()


    return data



def upload_page_image(
    job_id: str,
    page_number: int,
    image_bytes: bytes
):


    # Structure :
    # documents/pages/job_id/page_001.png


    object_name = (
        f"pages/{job_id}/page_{page_number:03}.png"
    )


    client.put_object(

        bucket_name=BUCKET_NAME,

        object_name=object_name,

        data=BytesIO(image_bytes),

        length=len(image_bytes),

        content_type="image/png"

    )


    return object_name