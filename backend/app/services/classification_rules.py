RULES = {

    "BC": [

        {
            "pattern": r"\bBON\s+DE\s+COMMANDE\b",
            "weight": 5
        },

        {
            "pattern": r"\bCOMMANDE\s+N[°O]?\b",
            "weight": 3
        },

        {
            "pattern": r"\bN[°O]?\s*BC\b",
            "weight": 2
        },

        {
            "pattern": r"\bBC[-/ ]?\d+\b",
            "weight": 2
        }

    ],


    "BL": [

        {
            "pattern": r"\bBON\s+DE\s+LIVRAISON\b",
            "weight": 5
        },

        {
            "pattern": r"\bBON\s+LIVRAISON\b",
            "weight": 4
        },

        {
            "pattern": r"\bN[°O]?\s*BL\b",
            "weight": 2
        },

        {
            "pattern": r"\bBL[-/ ]?\d+\b",
            "weight": 2
        }

    ],


    "FACTURE": [

        {
            "pattern": r"\bFACTURE\b",
            "weight": 5
        },

        {
            "pattern": r"\bINVOICE\b",
            "weight": 5
        },

        {
            "pattern": r"\bAVOIR\b",
            "weight": 4
        },

        {
            "pattern": r"\bN[°O]?\s*FAC\b",
            "weight": 3
        },

        {
            "pattern": r"\bFA[-/ ]?\d+\b",
            "weight": 2
        }

    ]

}