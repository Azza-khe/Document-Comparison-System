from app.models.document_group import DocumentGroup
from app.models.document_group_page import DocumentGroupPage

from app.services.reference_extractor import extract_reference
from app.services.continuation_detector import is_continuation


def group_pages(
    db,
    job_id,
    pages
):

    groups = []

    current_group = None


    for page in pages:

        reference = extract_reference(page)


        if current_group is None:

            current_group = {

                "doc_type": page.document_type,

                "ref_hint": reference,

                "confidence": page.classification_confidence,

                "pages": [page]

            }

            continue


        same_type = (
            page.document_type ==
            current_group["doc_type"]
        )

        same_reference = (
            reference is not None
            and
            reference ==
            current_group["ref_hint"]
        )


        continuation = is_continuation(page)


        if same_type and (
            same_reference
            or continuation
            or current_group["ref_hint"] is None
        ):

            current_group["pages"].append(page)

        else:

            groups.append(current_group)

            current_group = {

                "doc_type": page.document_type,

                "ref_hint": reference,

                "confidence": page.classification_confidence,

                "pages": [page]

            }


    if current_group:

        groups.append(current_group)


    saved_groups = []


    for group in groups:

        db_group = DocumentGroup(

            job_id=job_id,

            doc_type=group["doc_type"],

            ref_hint=group["ref_hint"],

            confidence=group["confidence"]

        )

        db.add(db_group)

        db.flush()


        for page in group["pages"]:

            db.add(

                DocumentGroupPage(

                    group_id=db_group.id,

                    page_id=page.id

                )

            )


        saved_groups.append(db_group)


    db.commit()

    for group in saved_groups:

      db.refresh(group)


    return saved_groups