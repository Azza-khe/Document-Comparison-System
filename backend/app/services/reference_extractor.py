import re


REFERENCE_PATTERNS = [

    # OM176453
    r"\bOM\s*\d{4,}\b",

    # BC2025001
    r"\bBC[- ]?\d+\b",

    # BL2025001
    r"\bBL[- ]?\d+\b",

    # FAC2025001
    r"\bFAC[- ]?\d+\b",

    # Facture N°
    r"FACTURE\s*N[°º:]?\s*([A-Z0-9\-]+)",

    # Bon de commande N°
    r"BON\s+DE\s+COMMANDE.*?([A-Z0-9]{5,})",

    # Bon de livraison N°
    r"BON\s+DE\s+LIVRAISON.*?([A-Z0-9]{5,})",
]


def extract_reference(page):
    """
    Extraction légère d'une référence documentaire.

    Utilisée uniquement par le Layer 4
    pour aider au regroupement.
    """

    text = page.raw_text or ""

    text = text.upper()

    for pattern in REFERENCE_PATTERNS:

        match = re.search(
            pattern,
            text,
            re.DOTALL
        )

        if match:

            if match.lastindex:

                ref = match.group(1)

            else:

                ref = match.group(0)

            ref = re.sub(
                r"\s+",
                "",
                ref
            )

            return ref

    return None