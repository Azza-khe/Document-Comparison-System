# app/services/extraction/native_extractor.py

import re



def merge_native_pages(pages):

    text = ""

    for page in pages:

        if page.raw_text:

            text += page.raw_text
            text += "\n"


    return text




def extract_lines_from_text(text):

    items = []


    IGNORE = [

        "FOURNISSEUR",
        "CLIENT",
        "SOCIETE",
        "SOCIÉTÉ",
        "ZONE INDUSTRIELLE",
        "ROUTE",
        "MF",
        "TOTAL",
        "TVA",
        "TTC",
        "CONDITIONS",
        "REFERENCE",
        "RÉFÉRENCE",
        "NUMERO",
        "NUMÉRO",
        "DATE",
        "SIGNATURE",
        "ECHEANCE",
        "ÉCHÉANCE"

    ]



    for line in text.split("\n"):


        line = line.strip()


        if not line:
            continue



        upper = line.upper()



        if any(word in upper for word in IGNORE):
            continue



        # récupérer les nombres
        numbers = re.findall(
            r"\d+(?:[.,]\d+)?",
            line
        )


        if not numbers:
            continue



        # =================================================
        # BL :
        # le dernier nombre est généralement la quantité
        # =================================================

        quantity_text = numbers[-1]


        try:

            quantity = float(
                quantity_text.replace(",", ".")
            )

            if quantity.is_integer():

                quantity = int(quantity)


        except:

            continue



        # =================================================
        # supprimer uniquement la quantité finale
        # garder les dimensions et références
        # =================================================


        description = re.sub(
            r"\s+\d+(?:[.,]\d+)?\s*$",
            "",
            line
        ).strip()



        if len(description) < 5:
            continue



        items.append({

            "reference": None,

            "description": description,

            "quantity": quantity,

            "unit": None,

            "unit_price": None,

            "total": None,

            "confidence": 0.7

        })


    return items