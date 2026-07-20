import pdfplumber


# =====================================================
# Extraction des tableaux PDF
# =====================================================

def extract_pdf_tables(
    pdf_path,
    pages_numbers
):

    tables = []

    with pdfplumber.open(pdf_path) as pdf:

        for page_number in pages_numbers:

            page = pdf.pages[page_number - 1]

            page_tables = []

            # ==================================
            # STRATEGIE 1
            # Tableau avec bordures
            # ==================================

            page_tables.extend(

                page.extract_tables(
                    {

                        "vertical_strategy": "lines",

                        "horizontal_strategy": "lines",

                        "snap_tolerance": 5,

                        "join_tolerance": 5,

                        "edge_min_length": 3

                    }

                ) or []

            )

            # ==================================
            # STRATEGIE 2
            # Tableau sans bordures
            # ==================================

            page_tables.extend(

                page.extract_tables(
                    {

                        "vertical_strategy": "text",

                        "horizontal_strategy": "text",

                        "text_x_tolerance": 3,

                        "text_y_tolerance": 3,

                        "intersection_tolerance": 3

                    }

                ) or []

            )

            # ==================================
            # STRATEGIE 3
            # Colonnes alignées
            # ==================================

            page_tables.extend(

                page.extract_tables(
                    {

                        "vertical_strategy": "text",

                        "horizontal_strategy": "lines",

                        "text_x_tolerance": 2,

                        "text_y_tolerance": 2

                    }

                ) or []

            )

            # ==================================
            # Nettoyage
            # ==================================

            for table in page_tables:

                if not table:
                    continue

                if len(table) < 2:
                    continue

                cleaned = []

                for row in table:

                    if row is None:
                        continue

                    if all(
                        cell is None or str(cell).strip() == ""
                        for cell in row
                    ):
                        continue

                    cleaned.append(row)

                if len(cleaned) > 1:
                    tables.append(cleaned)

    return tables