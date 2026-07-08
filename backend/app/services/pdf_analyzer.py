import fitz  # PyMuPDF

from app.models.page import Page


class PDFAnalyzer:
    """
    Layer 1
    PDF Analysis & Type Detection

    Responsibilities
    ----------------
    - Open PDF
    - Analyze every page
    - Extract native text
    - Compute image coverage ratio
    - Detect if page is NATIVE or SCANNED
    """

    # Thresholds
    MIN_CHAR_COUNT = 50
    MAX_NATIVE_IMAGE_RATIO = 0.30
    MIN_SCANNED_IMAGE_RATIO = 0.70

    def analyze(self, pdf_path: str) -> list[Page]:
        """
        Analyze all pages of a PDF.
        """

        document = fitz.open(pdf_path)

        analyzed_pages = []

        for page_index in range(len(document)):
            page = document.load_page(page_index)
            analyzed_pages.append(self._analyze_page(page))

        document.close()

        return analyzed_pages

    def get_total_pages(self, pdf_path: str) -> int:
        """
        Return the total number of pages.
        """

        document = fitz.open(pdf_path)
        total_pages = len(document)
        document.close()

        return total_pages

    def _analyze_page(self, page: fitz.Page) -> Page:

        # ----------------------------
        # Extract native text
        # ----------------------------

        raw_text = page.get_text("text")

        char_count = len(raw_text.strip())

        # ----------------------------
        # Page dimensions
        # ----------------------------

        width = page.rect.width
        height = page.rect.height

        page_area = width * height

        # ----------------------------
        # Images analysis
        # ----------------------------

        image_area = 0.0

        images = page.get_images(full=True)

        image_count = len(images)

        for image in images:

            xref = image[0]

            rects = page.get_image_rects(xref)

            for rect in rects:

                image_area += rect.width * rect.height

        if page_area > 0:
            image_coverage_ratio = image_area / page_area
        else:
            image_coverage_ratio = 0.0

        # ----------------------------
        # Detect source type
        # ----------------------------

        source_type = self._detect_source_type(
            char_count,
            image_coverage_ratio
        )

        # ----------------------------
        # Return Page object
        # ----------------------------

        return Page(
            page_number=page.number + 1,
            source_type=source_type,
            char_count=char_count,
            image_count=image_count,
            image_coverage_ratio=round(image_coverage_ratio, 3),
            width=round(width, 2),
            height=round(height, 2),
            raw_text=raw_text
        )

    def _detect_source_type(
        self,
        char_count: int,
        image_ratio: float
    ) -> str:
        """
        Determine whether the page is native or scanned.
        """

        if (
            char_count >= self.MIN_CHAR_COUNT
            and image_ratio <= self.MAX_NATIVE_IMAGE_RATIO
        ):
            return "NATIVE"

        if (
            char_count < self.MIN_CHAR_COUNT
            or image_ratio >= self.MIN_SCANNED_IMAGE_RATIO
        ):
            return "SCANNED"

        return "UNKNOWN"