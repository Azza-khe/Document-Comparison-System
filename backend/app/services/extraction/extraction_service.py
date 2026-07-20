from app.services.extraction.native_extractor import merge_native_pages
from app.services.extraction.supplier_detector import detect_supplier
from app.services.extraction.pdf_table_extractor import extract_pdf_tables

from app.services.extraction.bc_extractor import extract_bc
from app.services.extraction.bl_extractor import extract_bl
from app.services.extraction.facture_extractor import extract_facture

from app.models.extracted_document import ExtractedDocument
from app.models.extracted_item import ExtractedItem



def extract_document(
    group,
    pdf_path,
    db
):

    # ==========================================
    # Récupération des pages du groupe
    # ==========================================

    pages = [
        item.page
        for item in group.pages
    ]


    # ==========================================
    # Préparation extraction
    # ==========================================

    text = merge_native_pages(
        pages
    )


    page_numbers = [
        page.page_number
        for page in pages
    ]


    tables = extract_pdf_tables(
        pdf_path,
        page_numbers
    )


    supplier = detect_supplier(
        text
    )


    # ==========================================
    # Extraction selon type document
    # ==========================================

    if group.doc_type == "BC":

        data = extract_bc(
            text,
            tables,
            supplier
        )


    elif group.doc_type == "BL":

        data = extract_bl(
            text,
            tables,
            supplier
        )


    elif group.doc_type == "FACTURE":

        data = extract_facture(
            text,
            tables,
            supplier
        )


    else:

        data = {
            "doc_type": "UNKNOWN",
            "confidence": 0.0,
            "items": []
        }


    # ==========================================
    # Récupération confiance
    # ==========================================

    confidence = data.get(
        "confidence",
        0.0
    )


    # ==========================================
    # Création ExtractedDocument
    # ==========================================

    extracted_document = ExtractedDocument(

        document_group_id=group.id,

        doc_type=group.doc_type,

        extracted_data=data,

        confidence=confidence,

        extraction_source="RULE",

        extraction_status="COMPLETED"

    )


    # Ajout document
    db.add(
        extracted_document
    )


    # Premier flush pour récupérer extracted_document.id
    db.flush()



    # ==========================================
    # Sauvegarde des lignes produits
    # ==========================================

    items = data.get(
        "items",
        []
    )


    for index, item in enumerate(
        items,
        start=1
    ):

        extracted_item = ExtractedItem(

            document_id=extracted_document.id,

            line_number=index,

            product_code=item.get(
                "reference"
            ),

            description=item.get(
                "description"
            ),

            quantity=item.get(
                "quantity"
            ),

            unit=item.get(
                "unit"
            ),

            unit_price=item.get(
                "unit_price"
            ),

            discount=item.get(
                "discount"
            ),

            vat=item.get(
                "vat"
            ),

            total=item.get(
                "total"
            ),

            confidence=item.get(
                "confidence",
                0.0
            )

        )


        db.add(
            extracted_item
        )



    # ==========================================
    # Commit final
    # ==========================================

    db.commit()



    # Refresh
    db.refresh(
        extracted_document
    )


    return extracted_document