def calculate_table_score(text):

    lines = text.splitlines()

    count = 0

    for line in lines:

        if len(line.split()) >= 5:

            count += 1

    if count >= 10:
        return 2

    if count >= 5:
        return 1

    return 0