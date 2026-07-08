import os
import fitz


class PageRenderer:
    """
    Render every PDF page into PNG images.
    """

    DPI = 300

    def render(
        self,
        pdf_path: str,
        output_folder: str
    ) -> list[str]:

        document = fitz.open(pdf_path)

        os.makedirs(output_folder, exist_ok=True)

        saved_pages = []

        zoom = self.DPI / 72

        matrix = fitz.Matrix(zoom, zoom)

        for index in range(len(document)):

            page = document.load_page(index)

            pix = page.get_pixmap(matrix=matrix)

            filename = f"page_{index+1:03}.png"

            path = os.path.join(output_folder, filename)

            pix.save(path)

            saved_pages.append(path)

        document.close()

        return saved_pages