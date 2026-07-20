from app.services.extraction.header_extractor import extract_header

from app.services.extraction.item_extractor import extract_items



def extract_bl(
    text,
    tables,
    supplier
):


    items = extract_items(
        text,
        tables
    )



    return {


        "doc_type":"BL",


        "supplier":
            supplier,


        "header":
            extract_header(text),



        "items":
            items,


        "confidence":
            0.8

    }