import fitz



def inspect_pdf(pdf_path):


    document = fitz.open(pdf_path)


    pages = []


    for index, page in enumerate(document):


        text = page.get_text()


        character_count = len(
            text.strip()
        )


        images = page.get_images(
            full=True
        )


        image_count = len(images)



        page_area = (
            page.rect.width *
            page.rect.height
        )


        image_area = 0



        for img in images:

            xref = img[0]


            try:

                pix = fitz.Pixmap(
                    document,
                    xref
                )


                image_area += (
                    pix.width *
                    pix.height
                )


            except Exception:

                pass



        if page_area > 0:

            image_ratio = (
                image_area /
                page_area
            )

        else:

            image_ratio = 0



        # Classification Native / Scanned

        if (
            character_count > 50
            and image_ratio < 0.3
        ):

            source_type = "NATIVE"


        else:

            source_type = "SCANNED"



        pages.append({

            "page_number": index + 1,

            "source_type": source_type,

            "character_count": character_count,

            "image_count": image_count,

            "image_ratio": image_ratio,

            "width": page.rect.width,

            "height": page.rect.height,

            "raw_text": text

        })


    document.close()


    return pages