from app.services.pdf_inspector import inspect_pdf
from app.services.page_renderer import render_pages
from app.services.preprocessor import preprocess_scanned_pages

from app.models.page import Page



def analyze_job(
    db,
    job,
    pdf_path
):

    # =========================
    # Layer 1
    # Analyse PDF
    # native / scanned
    # =========================

    analysis = inspect_pdf(
        pdf_path
    )


    # =========================
    # Layer 1
    # PDF -> images dans MinIO
    # =========================

    images = render_pages(
        pdf_path,
        job.job_id
    )


    # =========================
    # Layer 2
    # Preprocessing uniquement
    # des pages SCANNED
    # =========================

    images = preprocess_scanned_pages(
        analysis,
        images
    )


    # =========================
    # Sauvegarde DB
    # =========================

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