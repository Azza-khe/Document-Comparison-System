START=[

"DESIGNATION",
"DESCRIPTION",
"ARTICLE",
"PRODUIT"

]


END=[

"TOTAL",
"TVA",
"TTC",
"CONDITIONS"

]



def detect_product_region(text):


    lines=text.split("\n")


    start=None
    end=None



    for i,line in enumerate(lines):


        if any(
            x in line.upper()
            for x in START
        ):

            start=i
            break



    if start is None:

        return text



    for i in range(start+1,len(lines)):


        if any(
            x in lines[i].upper()
            for x in END
        ):

            end=i
            break



    return "\n".join(
        lines[start:end]
    )