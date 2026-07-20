from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey
)

from sqlalchemy.orm import relationship

from app.core.database import Base


class ExtractedItem(Base):

    __tablename__ = "extracted_items"


    id = Column(
        Integer,
        primary_key=True
    )


    document_id = Column(
        Integer,
        ForeignKey(
            "extracted_documents.id"
        ),
        nullable=False
    )


    line_number = Column(
        Integer,
        nullable=False
    )


    product_code = Column(
        String,
        nullable=True
    )


    description = Column(
        String,
        nullable=False
    )


    quantity = Column(
        Float,
        nullable=True
    )


    unit = Column(
        String,
        nullable=True
    )


    unit_price = Column(
        Float,
        nullable=True
    )


    discount = Column(
        Float,
        nullable=True
    )


    vat = Column(
        Float,
        nullable=True
    )


    total = Column(
        Float,
        nullable=True
    )


    confidence = Column(
        Float,
        nullable=False
    )


    document = relationship(
        "ExtractedDocument",
        back_populates="items"
    )