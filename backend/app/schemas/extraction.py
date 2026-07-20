from typing import List
from typing import Optional

from pydantic import BaseModel


# ==========================================================
# Product Line
# One row from the products table
# ==========================================================

class ProductLine(BaseModel):

    line_number: Optional[int] = None

    reference: Optional[str] = None

    designation: Optional[str] = None

    quantity: Optional[float] = None

    unit: Optional[str] = None

    unit_price: Optional[float] = None

    total_ht: Optional[float] = None


# ==========================================================
# Supplier
# ==========================================================

class SupplierSchema(BaseModel):

    name: Optional[str] = None

    tax_id: Optional[str] = None

    vat_number: Optional[str] = None

    address: Optional[str] = None


# ==========================================================
# Customer
# ==========================================================

class CustomerSchema(BaseModel):

    name: Optional[str] = None

    tax_id: Optional[str] = None

    address: Optional[str] = None


# ==========================================================
# Totals
# ==========================================================

class TotalsSchema(BaseModel):

    total_ht: Optional[float] = None

    tax_amount: Optional[float] = None

    total_ttc: Optional[float] = None


# ==========================================================
# Main document extraction
# ==========================================================

class ExtractedDocumentSchema(BaseModel):

    doc_type: str

    reference: Optional[str] = None

    date: Optional[str] = None

    supplier: SupplierSchema

    customer: CustomerSchema

    totals: TotalsSchema

    lines: List[ProductLine] = []