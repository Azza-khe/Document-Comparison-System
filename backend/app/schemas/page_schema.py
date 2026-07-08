from pydantic import BaseModel


class PageSchema(BaseModel):

    page_number: int

    source_type: str

    char_count: int

    image_count: int

    image_coverage: float

    width: float

    height: float

    text: str