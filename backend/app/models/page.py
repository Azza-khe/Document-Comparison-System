from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    Text
)

from sqlalchemy.orm import relationship

from app.core.database import Base



class Page(Base):

    __tablename__ = "pages"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    job_id = Column(
        String,
        ForeignKey("jobs.job_id"),
        nullable=False
    )


    page_number = Column(
        Integer,
        nullable=False
    )


    source_type = Column(
        String,
        nullable=False
    )


    character_count = Column(
        Integer
    )


    image_count = Column(
        Integer
    )


    image_ratio = Column(
        Float
    )


    width = Column(
        Float
    )


    height = Column(
        Float
    )


    image_path = Column(
        String
    )


    raw_text = Column(
        Text
    )


    # ==================================================
    # Layer 3 - Page Classification
    # ==================================================


    document_type = Column(
        String,
        nullable=True
    )


    classification_confidence = Column(
        Float,
        nullable=True
    )


    classification_source = Column(
        String,
        nullable=True
    )


    # ==================================================
    # Relation avec Job
    # ==================================================

    job = relationship(
        "Job",
        back_populates="pages"
    )