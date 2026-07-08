import fitz



def inspect_pdf(pdf_path):


    document = fitz.open(pdf_path)


    pages=[]


    for index,page in enumerate(document):


        text = page.get_text()


        character_count = len(
            text.strip()
        )


        images = page.get_images(
            full=True
        )


        image_count = len(images)



        if image_count > 0:

            image_ratio = 0.8

        else:

            image_ratio = 0



        if character_count > 50:

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