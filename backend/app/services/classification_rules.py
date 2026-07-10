RULES = {

    "BC": [

        (r"\bBON\s+DE\s+COMMANDE\b", 5),
        (r"\bCOMMANDE\s+N[°O]?\b", 3),
        (r"\bBC[-/]", 2),
        (r"\bN[°O]?\s*BC\b", 2)

    ],


    "BL": [

        (r"\bBON\s+DE\s+LIVRAISON\b", 5),
        (r"\bLIVRAISON\s+N[°O]?\b", 3),
        (r"\bBL[-/]", 2),
        (r"\bN[°O]?\s*BL\b", 2)

    ],


    "FACTURE": [

        (r"\bFACTURE\b", 5),
        (r"\bINVOICE\b", 5),
        (r"\bFA[-/]", 2),
        (r"\bN[°O]?\s*FACTURE\b", 3)

    ]

}