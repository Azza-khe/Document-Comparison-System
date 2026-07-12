def calculate_confidence(
    keyword_score,
    regex_score,
    table_score
):

    score = keyword_score + regex_score + table_score

    if score >= 8:
        return 0.97

    if score >= 7:
        return 0.95

    if score >= 6:
        return 0.92

    if score >= 5:
        return 0.90

    if score >= 4:
        return 0.80

    if score >= 3:
        return 0.70

    return 0.0