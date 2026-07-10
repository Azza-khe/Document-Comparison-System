from minio import Minio
from io import BytesIO


# ===============================
# Configuration MinIO
# ===============================

client = Minio(
    "localhost:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False
)


BUCKET_NAME = "documents"



# ===============================
# Layer 0
# Upload PDF original
# ===============================

def upload_pdf(
    job_id: str,
    file_bytes: bytes
):

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



def download_pdf(
    object_name: str
):

    response = client.get_object(
        BUCKET_NAME,
        object_name
    )


    data = response.read()


    response.close()
    response.release_conn()


    return data





# ===============================
# Layer 1
# Render PDF pages
# ===============================

def upload_page_image(
    job_id: str,
    page_number: int,
    image_bytes: bytes
):

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





# ===============================
# Layer 2
# Télécharger image pour OpenCV
# ===============================

def download_image(
    object_name: str
):

    response = client.get_object(
        BUCKET_NAME,
        object_name
    )


    image_bytes = response.read()


    response.close()
    response.release_conn()


    return image_bytes





# ===============================
# Layer 2
# Remplacer l'image existante
# après preprocessing
# ===============================

def update_page_image(
    object_name: str,
    image_bytes: bytes
):


    client.put_object(

        bucket_name=BUCKET_NAME,

        object_name=object_name,

        data=BytesIO(image_bytes),

        length=len(image_bytes),

        content_type="image/png"

    )


    return object_name