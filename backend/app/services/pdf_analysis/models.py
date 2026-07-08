from dataclasses import dataclass
from typing import List

from .page_info import PageInfo


@dataclass
class PDFAnalysisResult:

    total_pages: int

    pages: List[PageInfo]