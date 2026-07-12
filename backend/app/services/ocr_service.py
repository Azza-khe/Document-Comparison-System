from app.services.ocr_engine import extract_text_from_image



def process_ocr(
    db,
    pages
):


    for page in pages:


        # OCR seulement pour les pages scannées
        if page.source_type == "SCANNED":


            text = extract_text_from_image(
                page.image_path
            )


            page.raw_text = text


            db.add(page)



    db.commit()


    return pages