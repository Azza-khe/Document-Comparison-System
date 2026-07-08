from app.services.pdf_analyzer import PDFAnalyzer

class AnalyzeService:

    def __init__(self):
        self.analyzer = PDFAnalyzer()

    def analyze_pdf(self, pdf_path: str):
        return self.analyzer.analyze(pdf_path)