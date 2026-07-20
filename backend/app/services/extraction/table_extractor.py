import re

from app.services.extraction.column_aliases import COLUMN_ALIASES



# =====================================================
# Normalisation
# =====================================================

def normalize(value):

    if value is None:
        return ""

    return (
        str(value)
        .lower()
        .strip()
        .replace("\n", " ")
    )



# =====================================================
# Conversion nombre
# =====================================================

def convert_number(value):

    if value is None:
        return None

    value = (
        str(value)
        .replace("\n", "")
        .replace(" ", "")
        .replace(",", ".")
    )

    try:

        number = float(value)

        if number.is_integer():
            return int(number)

        return number

    except:

        return None



# =====================================================
# Détection colonnes
# =====================================================

def detect_columns(headers):

    mapping = {}

    for index, header in enumerate(headers):

        header = normalize(header)


        for field, aliases in COLUMN_ALIASES.items():

            for alias in aliases:

                alias = normalize(alias)


                if alias in header:

                    mapping[index] = field
                    break


    return mapping



# =====================================================
# Validation description
# =====================================================

def valid_description(text):

    if not text:
        return False


    text = str(text).strip()


    if len(text) < 3:
        return False



    if re.fullmatch(
        r"[\d\s.,]+",
        text
    ):
        return False



    forbidden = [

        "TOTAL",
        "TVA",
        "TTC",
        "SOUS TOTAL",
        "MONTANT",
        "NET A PAYER",
        "NET À PAYER"

    ]


    upper = text.upper()


    for word in forbidden:

        if word in upper:
            return False


    return True



# =====================================================
# Confidence
# =====================================================

def calculate_confidence(item):

    confidence = 0


    if item["description"]:
        confidence += 0.5


    if item["reference"]:
        confidence += 0.1


    if item["quantity"] is not None:
        confidence += 0.25


    if item["unit_price"] is not None:
        confidence += 0.05


    if item["total"] is not None:
        confidence += 0.10


    return round(
        confidence,
        2
    )



# =====================================================
# Extraction tableau
# =====================================================

def extract_table_rows(table):

    if not table:
        return []


    if len(table) < 2:
        return []



    headers = table[0]


    column_map = detect_columns(
        headers
    )



    if not column_map:

        return []



    items = []



    for row in table[1:]:


        if not row:
            continue



        if all(
            cell is None or str(cell).strip() == ""
            for cell in row
        ):
            continue



        item = {

            "reference": None,

            "description": None,

            "quantity": None,

            "unit": None,

            "unit_price": None,

            "total": None,

            "confidence": 0

        }



        for index, value in enumerate(row):


            if index not in column_map:
                continue



            field = column_map[index]



            if field == "description":

                if value:

                    item["description"] = (
                        str(value)
                        .strip()
                    )



            elif field == "reference":

                if value:

                    item["reference"] = (
                        str(value)
                        .strip()
                    )



            elif field == "quantity":

                item["quantity"] = convert_number(
                    value
                )



            elif field == "unit":

                item["unit"] = str(
                    value
                ).strip()



            elif field == "unit_price":

                item["unit_price"] = convert_number(
                    value
                )



            elif field == "total":

                item["total"] = convert_number(
                    value
                )



        # ======================================
        # Cas BL :
        # description + quantité suffisent
        # ======================================

        if not valid_description(
            item["description"]
        ):

            continue



        if (
            item["quantity"] is None
            and item["unit_price"] is None
            and item["total"] is None
        ):

            continue



        item["confidence"] = calculate_confidence(
            item
        )


        items.append(item)



    return items