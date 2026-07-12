import re



def extract_reference(page):


    text = page.raw_text or ""


    patterns=[

        r"BC[-\s]?\d+",

        r"BL[-\s]?\d+",

        r"FAC[-\s]?\d+",

        r"\bOM\d+\b",

        r"\bFL\d+\b"

    ]


    for p in patterns:


        match=re.search(
            p,
            text,
            re.I
        )


        if match:

            return match.group()



    return None