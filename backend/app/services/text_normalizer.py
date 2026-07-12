import re
import unicodedata


def normalize_text(text):

    if not text:
        return ""

    text = text.upper()

    text = unicodedata.normalize(
        "NFD",
        text
    )

    text = "".join(

        c

        for c in text

        if unicodedata.category(c) != "Mn"

    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()