import re


# =====================================================
# Référence du document (BC / BL / FA)
# =====================================================

DOCUMENT_PATTERNS = [

    r"\b(?:BC|BL|FA)-\d{4}/\d+\b",

    r"\b(?:BC|BL|FA)[-/]\d{4}[-/]\d+\b",

    r"(?:Num[eé]ro|N°|No)\s*[:\-]?\s*((?:BC|BL|FA)-?\d{4}/\d+)",

]


# =====================================================
# Références liées
# =====================================================

BC_PATTERN = r"Référence\s+commande\s*:\s*(BC-\d{4}/\d+)"
BL_PATTERN = r"Référence\s+livraison\s*:\s*(BL-\d{4}/\d+)"


# =====================================================
# Date
# =====================================================

DATE_PATTERNS = [

    r"Date\s*[:\-]?\s*(\d{2}[/-]\d{2}[/-]\d{4})",

    r"\b(\d{2}[/-]\d{2}[/-]\d{4})\b"

]


# =====================================================
# Extraction document principal
# =====================================================

def extract_reference(text):

    for pattern in DOCUMENT_PATTERNS:

        result = re.search(
            pattern,
            text,
            re.I
        )

        if result:

            if result.lastindex:
                return result.group(1)

            return result.group()

    return None


# =====================================================
# Extraction BC liée
# =====================================================

def extract_bc_reference(text):

    result = re.search(
        BC_PATTERN,
        text,
        re.I
    )

    if result:
        return result.group(1)

    return None


# =====================================================
# Extraction BL liée
# =====================================================

def extract_bl_reference(text):

    result = re.search(
        BL_PATTERN,
        text,
        re.I
    )

    if result:
        return result.group(1)

    return None


# =====================================================
# Date
# =====================================================

def extract_date(text):

    for pattern in DATE_PATTERNS:

        result = re.search(
            pattern,
            text,
            re.I
        )

        if result:

            return result.group(1)

    return None


# =====================================================
# Header complet
# =====================================================

def extract_header(text):

    return {

        "reference": extract_reference(text),

        "date": extract_date(text),

        "bc_reference": extract_bc_reference(text),

        "bl_reference": extract_bl_reference(text)

    }