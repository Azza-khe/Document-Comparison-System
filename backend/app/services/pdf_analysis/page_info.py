from dataclasses import dataclass


@dataclass
class PageInfo:
    page_number: int
    width: float
    height: float

    char_count: int
    image_count: int
    image_area_ratio: float

    source_type: str

    raw_text: str