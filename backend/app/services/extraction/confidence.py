def calculate_confidence(data):


    required = [

        "supplier",

        "header",

        "items"

    ]


    score = 0


    for field in required:


        if data.get(field):

            score += 1



    return round(

        score / len(required),

        2

    )