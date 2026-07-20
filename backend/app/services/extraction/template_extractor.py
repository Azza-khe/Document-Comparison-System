from app.services.extraction.header_extractor import extract_header
from app.services.extraction.item_extractor import extract_items
from app.services.extraction.totals_extractor import extract_totals



def extract_template(
    doc_type,
    text,
    tables,
    supplier
):


    data={


        "doc_type":doc_type,


        "supplier":supplier,


        "header":
            extract_header(text),


        "items":
            extract_items(
                text,
                tables,
                supplier.get("profile")
            ),


        "confidence":0.8

    }



    if doc_type=="FACTURE":


        data["totals"]=extract_totals(
            text
        )



    return data