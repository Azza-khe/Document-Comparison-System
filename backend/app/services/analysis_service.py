from app.services.pdf_inspector import inspect_pdf
from app.services.page_renderer import render_pages

from app.models.page import Page



def analyze_job(
    db,
    job,
    pdf_path
):

    # Analyse des pages du PDF
    analysis = inspect_pdf(
        pdf_path
    )


    # Conversion des pages PDF en images
    images = render_pages(
        pdf_path,
        job.job_id
    )


    pages = []


    for data, image in zip(
        analysis,
        images
    ):

        page = Page(

            job_id=job.job_id,

            image_path=image,

            **data

        )


        db.add(page)

        pages.append(page)



    job.status = "ANALYZED"


    db.commit()


    return pages