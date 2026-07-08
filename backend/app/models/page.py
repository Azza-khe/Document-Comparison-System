from dataclasses import dataclass


@dataclass
class Page:
    page_number: int

    source_type: str

    char_count: int

    image_count: int

    image_coverage: float

    width: float

    height: float

    text: str