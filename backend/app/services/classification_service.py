from app.services.classifier import classify_page



def classify_pages(
    db,
    pages
):


    classified_pages = []


    for page in pages:


        result = classify_page(
            page
        )


        page.document_type = result["document_type"]

        page.classification_confidence = result["confidence"]

        page.classification_source = result["source"]



        db.add(page)


        classified_pages.append(page)



    db.commit()


    return classified_pages