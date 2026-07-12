from app.services.rule_classifier import classify_by_rules
from app.services.ai_classifier import classify_by_ai
from app.services.review_queue import create_review_task


def classify_pages(db, pages):

    for page in pages:

        # -------------------------
        # Tier 1
        # -------------------------

        result = classify_by_rules(page)

        # -------------------------
        # Tier 2
        # -------------------------

        if result["confidence"] < 0.90:
            result = classify_by_ai(page)

        # -------------------------
        # Tier 3
        # -------------------------

        if result["confidence"] < 0.70:
            result = create_review_task(
                db,
                page
            )
            return result 

        page.document_type = result["document_type"]
        page.classification_confidence = result["confidence"]
        page.classification_source = result["source"]

        db.add(page)

    db.commit()

    return pages