import cv2
import numpy as np
import pytesseract
import re


from app.services.storage import (
    download_image,
    update_page_image
)


# =====================================================
# 1. Orientation Detection (Tesseract OSD)
# =====================================================

def detect_orientation(image):

    try:

        osd = pytesseract.image_to_osd(
            image
        )

        match = re.search(
            r"Rotate:\s+(\d+)",
            osd
        )

        if match:

            return int(
                match.group(1)
            )

    except Exception:

        pass


    return 0



# =====================================================
# 2. Orientation Correction
# =====================================================

def correct_orientation(image):

    angle = detect_orientation(
        image
    )


    if angle == 90:

        image = cv2.rotate(
            image,
            cv2.ROTATE_90_CLOCKWISE
        )


    elif angle == 180:

        image = cv2.rotate(
            image,
            cv2.ROTATE_180
        )


    elif angle == 270:

        image = cv2.rotate(
            image,
            cv2.ROTATE_90_COUNTERCLOCKWISE
        )


    return image



# =====================================================
# 3. Deskew
# Correction petites rotations scanner
# =====================================================

def deskew(image):

    try:

        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )


        coords = np.column_stack(
            np.where(
                gray < 255
            )
        )


        if len(coords) < 10:

            return image



        angle = cv2.minAreaRect(
            coords
        )[-1]


        if angle < -45:

            angle = 90 + angle



        if abs(angle) > 15:

            return image



        center = (

            image.shape[1] // 2,

            image.shape[0] // 2

        )


        matrix = cv2.getRotationMatrix2D(

            center,

            angle,

            1.0

        )


        corrected = cv2.warpAffine(

            image,

            matrix,

            (
                image.shape[1],
                image.shape[0]
            ),

            flags=cv2.INTER_CUBIC,

            borderMode=cv2.BORDER_REPLICATE

        )


        return corrected



    except Exception:


        return image



# =====================================================
# 4. Grayscale
# =====================================================

def to_grayscale(image):

    return cv2.cvtColor(

        image,

        cv2.COLOR_BGR2GRAY

    )



# =====================================================
# 5. Denoise
# Gaussian Blur
# =====================================================

def denoise(image):

    return cv2.GaussianBlur(

        image,

        (5,5),

        0

    )



# =====================================================
# 6. Binarization
# Otsu Threshold
# =====================================================

def binarize(image):

    _, binary = cv2.threshold(

        image,

        0,

        255,

        cv2.THRESH_BINARY +

        cv2.THRESH_OTSU

    )


    return binary



# =====================================================
# 7. Border Removal
# =====================================================

def remove_borders(image):

    try:

        inverted = 255 - image


        coords = cv2.findNonZero(

            inverted

        )


        if coords is None:

            return image



        x,y,w,h = cv2.boundingRect(

            coords

        )


        padding = 5


        x = max(

            0,

            x-padding

        )


        y = max(

            0,

            y-padding

        )


        w = min(

            image.shape[1]-x,

            w+2*padding

        )


        h = min(

            image.shape[0]-y,

            h+2*padding

        )



        return image[

            y:y+h,

            x:x+w

        ]


    except Exception:


        return image



# =====================================================
# MAIN PIPELINE LAYER 2
# =====================================================

def preprocess_image(

    image_object_name:str

):


    # ---------------------------------
    # Download image from MinIO
    # ---------------------------------

    image_bytes = download_image(

        image_object_name

    )


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

            f"Impossible de lire {image_object_name}"

        )



    # =================================
    # Layer 2 Pipeline
    # =================================


    # 1 - Orientation detection
    image = correct_orientation(

        image

    )


    # 2 - Deskew
    image = deskew(

        image

    )


    # 3 - Grayscale
    image = to_grayscale(

        image

    )


    # 4 - Denoise
    image = denoise(

        image

    )


    # 5 - Binarization Otsu
    image = binarize(

        image

    )


    # 6 - Border removal
    image = remove_borders(

        image

    )


    # ---------------------------------
    # Save processed image
    # ---------------------------------

    success, buffer = cv2.imencode(

        ".png",

        image

    )


    if not success:

        raise ValueError(

            "Erreur encodage PNG"

        )


    processed_bytes = buffer.tobytes()



    update_page_image(

        image_object_name,

        processed_bytes

    )


    return image_object_name




# =====================================================
# Apply Layer 2 only on scanned pages
# =====================================================

def preprocess_scanned_pages(

    analysis,

    images

):


    processed_images = []


    for data, image in zip(

        analysis,

        images

    ):



        if data["source_type"] == "SCANNED":


            processed = preprocess_image(

                image

            )


            processed_images.append(

                processed

            )


        else:


            # Native PDF :
            # aucune modification

            processed_images.append(

                image

            )


    return processed_images