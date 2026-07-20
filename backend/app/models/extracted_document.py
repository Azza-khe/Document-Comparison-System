from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    JSON,
    DateTime
)

from sqlalchemy.orm import relationship

from datetime import datetime

from app.core.database import Base


class ExtractedDocument(Base):

    __tablename__ = "extracted_documents"


    id = Column(
        Integer,
        primary_key=True
    )


    document_group_id = Column(
        Integer,
        ForeignKey(
            "document_groups.id"
        ),
        nullable=False,
        unique=True
    )


    doc_type = Column(
        String,
        nullable=False
    )


    extracted_data = Column(
        JSON,
        nullable=False
    )


    confidence = Column(
        Float,
        nullable=False
    )


    extraction_source = Column(
        String,
        nullable=False
    )


    extraction_status = Column(
        String,
        nullable=False
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


    group = relationship(
        "DocumentGroup",
        back_populates="extracted_document"
    )


    items = relationship(
        "ExtractedItem",
        back_populates="document",
        cascade="all, delete-orphan"
    )