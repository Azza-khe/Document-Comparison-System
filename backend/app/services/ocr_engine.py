import pytesseract

from PIL import Image

from io import BytesIO



# Chemin Tesseract Windows

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)



def extract_text_from_image(
    image_bytes: bytes
):


    image = Image.open(
        BytesIO(image_bytes)
    )


    text = pytesseract.image_to_string(
        image,
        lang="fra"
    )


    return text.strip()