import re


REFERENCE_PATTERNS = {

    "BC": r"\bBC[- ]?\d{3,}\b",

    "BL": r"\bBL[- ]?\d{3,}\b",

    "FACTURE": r"\b(FAC|FACT)[- ]?\d{3,}\b"

}


def has_reference(
    text,
    document_type
):

    pattern = REFERENCE_PATTERNS.get(
        document_type
    )

    if pattern is None:
        return False

    return bool(
        re.search(
            pattern,
            text
        )
    )