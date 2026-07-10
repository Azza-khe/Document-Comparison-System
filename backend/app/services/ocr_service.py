from app.services.ocr_engine import extract_text_from_image

from app.services.storage import download_image



def process_ocr(
    db,
    pages
):


    for page in pages:


        # OCR uniquement les scans

        if page.source_type != "SCANNED":

            continue



        print(
            "OCR PAGE:",
            page.page_number
        )


        image_bytes = download_image(
            page.image_path
        )


        text = extract_text_from_image(
            image_bytes
        )


        page.raw_text = text


        page.character_count = len(text)


        db.add(page)



    db.commit()


    return pages