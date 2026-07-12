import re


PATTERNS = [

    r"page\s+\d+\s+sur\s+\d+",

    r"page\s+\d+\s+of\s+\d+",

    r"suite",

    r"continuation"

]


def is_continuation(page):

    text = (
        page.raw_text or ""
    ).lower()

    for pattern in PATTERNS:

        if re.search(pattern, text):

            return True

    return False