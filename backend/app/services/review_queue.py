from app.models.review_queue import ReviewQueue


def create_review_task(
    db,
    page
):
    """
    Tier 3 - Human Review Queue
    """


    review = ReviewQueue(

        page_id=page.id,

        document_type="UNKNOWN",

        confidence=0.0,

        status="PENDING"

    )


    # ============================
    # Update page classification
    # ============================

    page.document_type = "UNKNOWN"

    page.classification_confidence = 0.0

    page.classification_source = "HUMAN_REVIEW"



    # Ajouter la tâche review

    db.add(review)


    # Sauvegarder les deux modifications

    db.commit()


    db.refresh(review)



    return {

        "page_id": page.id,

        "document_type": "UNKNOWN",

        "confidence": 0.0,

        "source": "HUMAN_REVIEW",

        "status": "PENDING"

    }