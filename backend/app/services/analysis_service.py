from app.services.pdf_inspector import inspect_pdf
from app.services.page_renderer import render_pages
from app.services.preprocessor import preprocess_scanned_pages

from app.services.ocr_service import process_ocr

from app.services.classification_service import classify_pages

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
    # Conversion PDF -> images
    # =========================

    images = render_pages(
        pdf_path,
        job.job_id
    )



    # =========================
    # Layer 2
    # Preprocessing scans
    # =========================

    images = preprocess_scanned_pages(
        analysis,
        images
    )



    # =========================
    # Création Pages
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



    db.commit()



    # =========================
    # OCR Layer
    # uniquement SCANNED
    # =========================

    pages = process_ocr(
        db,
        pages
    )



    # =========================
    # Layer 3
    # Classification
    # =========================

    pages = classify_pages(
        db,
        pages
    )



    # =========================
    # Job terminé
    # =========================

    job.status = "ANALYZED"


    db.commit()


    return pages