import re

from app.services.classification_rules import RULES



def classify_by_rules(page):


    text = page.raw_text or ""

    text = text.upper()


    # =========================
    # Priorité aux titres
    # =========================


    if re.search(
        r"\bBON\s+DE\s+LIVRAISON\b",
        text[:200]
    ):

        return {

            "document_type": "BL",

            "confidence": 0.95,

            "source": "RULE"

        }



    if re.search(
        r"\bBON\s+DE\s+COMMANDE\b",
        text[:200]
    ):

        return {

            "document_type": "BC",

            "confidence": 0.95,

            "source": "RULE"

        }



    if re.search(
        r"\bFACTURE\b",
        text[:200]
    ):

        return {

            "document_type": "FACTURE",

            "confidence": 0.95,

            "source": "RULE"

        }



    # =========================
    # Sinon scoring
    # =========================


    scores = {

        "BC": 0,

        "BL": 0,

        "FACTURE": 0

    }



    for document_type, patterns in RULES.items():


        for pattern, weight in patterns:


            if re.search(pattern, text):

                scores[document_type] += weight



    print(
        "CLASSIFICATION SCORES:",
        scores
    )



    best_type = max(
        scores,
        key=scores.get
    )


    if scores[best_type] == 0:

        return None



    return {

        "document_type": best_type,

        "confidence": min(
            0.95,
            0.75 + scores[best_type] * 0.05
        ),

        "source": "RULE"

    }