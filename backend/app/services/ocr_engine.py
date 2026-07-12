from PIL import Image
from io import BytesIO
import pytesseract

from app.services.storage import download_image


pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def extract_text_from_image(image_path: str):

    image_bytes = download_image(
        image_path
    )

    image = Image.open(
        BytesIO(image_bytes)
    )

    text = pytesseract.image_to_string(
        image,
        lang="fra"
    )

    return text