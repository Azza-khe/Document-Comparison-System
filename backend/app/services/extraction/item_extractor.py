from app.services.extraction.table_extractor import extract_table_rows
from app.services.extraction.native_extractor import extract_lines_from_text


# =====================================================
# Extraction des articles
# =====================================================

def extract_items(
    text,
    tables
):

    items = []

    # ==================================
    # TIER 1
    # Extraction des tableaux PDF
    # ==================================

    if tables:

        for table in tables:

            rows = extract_table_rows(table)

            if rows:
                items.extend(rows)

    # ==================================
    # Si des produits ont été trouvés
    # ==================================

    if items:

        return filter_valid_items(items)

    # ==================================
    # TIER 2
    # Extraction depuis le texte natif
    # ==================================

    items = extract_lines_from_text(text)

    return filter_valid_items(items)


# =====================================================
# Validation des produits
# =====================================================

def filter_valid_items(items):

    valid = []

    forbidden = [

        "BON DE COMMANDE",
        "BON DE LIVRAISON",
        "FACTURE",

        "FOURNISSEUR",
        "CLIENT",

        "NUMERO",
        "NUMÉRO",
        "N°",

        "DATE",

        "REFERENCE",
        "RÉFÉRENCE",

        "BC-",
        "BL-",
        "FA-",

        "MF",

        "MATRICULE",

        "SOCIETE",
        "SOCIÉTÉ",

        "ZONE",
        "ROUTE",
        "ADRESSE",

        "TOTAL",
        "TOTAL HT",
        "TOTAL TTC",

        "TVA",

        "CONDITION",
        "CONDITIONS",

        "ECHEANCE",
        "ÉCHÉANCE",

        "SIGNATURE",

        "LIVRAISON",
        "COMMANDE"

    ]

    seen = set()

    for item in items:

        description = (
            item.get("description")
            or ""
        ).strip()

        if not description:
            continue

        upper = description.upper()

        # ignorer lignes administratives
        if any(word in upper for word in forbidden):
            continue

        # uniquement numérique
        if upper.replace(",", "").replace(".", "").replace(" ", "").isdigit():
            continue

        # description trop courte
        if len(description) < 5:
            continue

        # éviter les doublons
        key = (
            description,
            item.get("quantity"),
            item.get("unit_price"),
            item.get("total")
        )

        if key in seen:
            continue

        seen.add(key)

        valid.append(item)

    return valid