import cv2
import numpy as np

from app.services.storage import (
    download_image,
    update_page_image
)


def to_grayscale(image):

    return cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )


def denoise(image):

    return cv2.GaussianBlur(
        image,
        (5, 5),
        0
    )


def deskew(image):
    """
    Corrige automatiquement
    une légère rotation.
    """

    coords = np.column_stack(
        np.where(image < 255)
    )

    if len(coords) == 0:
        return image

    angle = cv2.minAreaRect(coords)[-1]

    if angle < -45:
        angle = 90 + angle

    center = (
        image.shape[1] // 2,
        image.shape[0] // 2
    )

    matrix = cv2.getRotationMatrix2D(
        center,
        angle,
        1.0
    )

    return cv2.warpAffine(
        image,
        matrix,
        (image.shape[1], image.shape[0]),
        flags=cv2.INTER_CUBIC,
        borderMode=cv2.BORDER_REPLICATE
    )


def binarize(image):

    _, image = cv2.threshold(
        image,
        0,
        255,
        cv2.THRESH_BINARY +
        cv2.THRESH_OTSU
    )

    return image


def preprocess_image(
    image_object_name: str
):

    # =========================
    # 1) Télécharger depuis MinIO
    # =========================

    image_bytes = download_image(
        image_object_name
    )

    # =========================
    # 2) Bytes -> Image OpenCV
    # =========================

    image_array = np.frombuffer(
        image_bytes,
        np.uint8
    )

    image = cv2.imdecode(
        image_array,
        cv2.IMREAD_COLOR
    )

    if image is None:

        raise ValueError(
            f"Impossible de décoder {image_object_name}"
        )

    # =========================
    # 3) Prétraitement
    # =========================

    image = to_grayscale(
        image
    )

    image = denoise(
        image
    )

    image = deskew(
        image
    )

    image = binarize(
        image
    )

    # =========================
    # 4) Image -> PNG bytes
    # =========================

    success, buffer = cv2.imencode(
        ".png",
        image
    )

    if not success:

        raise ValueError(
            "Erreur d'encodage de l'image"
        )

    processed_bytes = buffer.tobytes()

    # =========================
    # 5) Remplacer l'image
    #    dans MinIO
    # =========================

    update_page_image(
        image_object_name,
        processed_bytes
    )

    return image_object_name


def preprocess_scanned_pages(
    analysis,
    images
):
    """
    Layer 2

    Prétraite uniquement
    les pages scannées.
    """

    processed_images = []

    for data, image in zip(
        analysis,
        images
    ):

        if data["source_type"] == "SCANNED":

            image = preprocess_image(
                image
            )

        processed_images.append(
            image
        )

    return processed_images

