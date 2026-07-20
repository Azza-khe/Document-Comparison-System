import re



# =====================================================
# Convert number
# =====================================================

def convert_amount(value):

    if not value:
        return None


    value = (
        value
        .replace(" ", "")
        .replace("\n", "")
        .replace(",", ".")
    )


    try:

        return float(value)

    except:

        return None




# =====================================================
# Generic amount extractor
# =====================================================

def extract_amount(
    text,
    label
):


    pattern = (
        label
        +
        r".{0,20}?"
        r"(\d[\d\s]*[.,]?\d*)"
    )


    result = re.search(
        pattern,
        text,
        re.I | re.S
    )


    if result:


        return convert_amount(
            result.group(1)
        )


    return None




# =====================================================
# TVA extractor
# =====================================================

def extract_tva(text):


    pattern = (
        r"TVA"
        r"\s*\d+%"
        r".{0,20}?"
        r"(\d[\d\s]*[.,]?\d*)"
    )


    result = re.search(
        pattern,
        text,
        re.I | re.S
    )


    if result:

        return convert_amount(
            result.group(1)
        )


    return None




# =====================================================
# Totals extractor
# =====================================================

def extract_totals(text):


    return {


        "total_ht":
            extract_amount(
                text,
                r"TOTAL\s*HT"
            ),


        "tva":
            extract_tva(
                text
            ),


        "total_ttc":
            extract_amount(
                text,
                r"TOTAL\s*TTC"
            )

    }