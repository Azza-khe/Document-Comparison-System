import fitz


def calculate_image_ratio(page: fitz.Page):

    images = page.get_images(full=True)

    if len(images) == 0:
        return 0.0, 0

    page_area = page.rect.width * page.rect.height

    total_image_area = 0

    for image in images:

        xref = image[0]

        try:

            rects = page.get_image_rects(xref)

            for rect in rects:

                total_image_area += rect.width * rect.height

        except:

            continue

    ratio = min(total_image_area / page_area, 1)

    return ratio, len(images)