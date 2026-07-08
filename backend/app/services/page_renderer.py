import fitz
from io import BytesIO

from app.services.storage import upload_page_image



def render_pages(
    pdf_path,
    job_id
):

    document = fitz.open(pdf_path)

    images=[]


    for index,page in enumerate(document):


        pix = page.get_pixmap(
            dpi=300
        )


        image_bytes = pix.tobytes(
            "png"
        )


        object_name = upload_page_image(
            job_id,
            index+1,
            image_bytes
        )


        images.append(
            object_name
        )


    document.close()


    return images