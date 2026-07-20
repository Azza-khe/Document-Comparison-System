from app.services.extraction.header_extractor import extract_header
from app.services.extraction.totals_extractor import extract_totals

from app.services.extraction.item_extractor import extract_items



def extract_bc(
    text,
    tables,
    supplier
):


    items = extract_items(
        text,
        tables
    )



    return {

        "doc_type":"BC",


        "supplier":
            supplier,


        "header":
            extract_header(text),



        "totals":
            extract_totals(text),



        "items":
            items,


        "confidence":
            0.8

    }