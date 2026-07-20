from app.services.pdf_inspector import inspect_pdf
from app.services.page_renderer import render_pages
from app.services.preprocessor import preprocess_scanned_pages

from app.services.ocr_service import process_ocr

from app.services.classification_service import classify_pages

from app.models.page import Page

from app.services.grouping_service import group_pages

from app.services.extraction.extraction_service import extract_document



def analyze_job(
    db,
    job,
    pdf_path
):


    # ==================================================
    # LAYER 1
    # PDF ANALYSIS
    # ==================================================

    analysis = inspect_pdf(
        pdf_path
    )



    # ==================================================
    # RENDER PAGES
    # ==================================================

    images = render_pages(
        pdf_path,
        job.job_id
    )



    # ==================================================
    # LAYER 2
    # PREPROCESSING
    # ==================================================

    images = preprocess_scanned_pages(
        analysis,
        images
    )



    # ==================================================
    # CREATE PAGES
    # ==================================================

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



    # ==================================================
    # OCR
    # ==================================================

    pages = process_ocr(
        db,
        pages
    )



    # ==================================================
    # LAYER 3
    # CLASSIFICATION
    # ==================================================

    pages = classify_pages(
        db,
        pages
    )



    # ==================================================
    # LAYER 4
    # GROUPING
    # ==================================================

    groups = group_pages(

        db,

        job.job_id,

        pages

    )



    # ==================================================
    # LAYER 5
    # EXTRACTION
    #
    # DocumentGroup
    #       |
    #       v
    # ExtractedDocument
    # ExtractedItem
    #
    # ==================================================

    for group in groups:


        extract_document(

            group,

            pdf_path,

            db

        )



    # ==================================================
    # UPDATE JOB STATUS
    # ==================================================

    job.status = "ANALYZED"


    db.commit()



    return pages