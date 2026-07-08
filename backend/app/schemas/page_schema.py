from pydantic import BaseModel



class PageResponse(BaseModel):

    page_number:int

    source_type:str

    character_count:int

    image_count:int

    image_ratio:float

    width:float

    height:float

    image_path:str


    class Config:

        from_attributes=True