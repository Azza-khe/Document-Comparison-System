import re

from app.services.classification_rules import RULES
from app.services.regex_rules import has_reference
from app.services.table_heuristic import calculate_table_score
from app.services.text_normalizer import normalize_text
from app.services.confidence_engine import calculate_confidence


HEADER_RATIO = 0.20


def classify_by_rules(page):

    # ============================
    # Normalisation
    # ============================

    text = normalize_text(
        page.raw_text or ""
    )

    # ============================
    # Texte vide
    # ============================

    if not text.strip():

        return {
            "document_type": "UNKNOWN",
            "confidence": 0.0,
            "source": "RULE_ENGINE"
        }

    # ============================
    # Seulement le haut de la page
    # ============================

    header = text[:max(200, int(len(text) * HEADER_RATIO))]

    best_document = "UNKNOWN"
    best_confidence = 0.0

    # ============================
    # Evaluation des règles
    # ============================

    for document_type, rules in RULES.items():

        keyword_score = 0

        for rule in rules:

            if re.search(
                rule["pattern"],
                header,
                re.IGNORECASE
            ):

                keyword_score += rule["weight"]

        regex_score = 0

        if has_reference(
            text,
            document_type
        ):
            regex_score = 2

        table_score = calculate_table_score(
            text
        )

        confidence = calculate_confidence(
            keyword_score,
            regex_score,
            table_score
        )

        if confidence > best_confidence:

            best_confidence = confidence
            best_document = document_type

    # ============================
    # Retour du meilleur résultat
    # ============================

    return {

        "document_type": best_document,

        "confidence": best_confidence,

        "source": "RULE_ENGINE"

    }