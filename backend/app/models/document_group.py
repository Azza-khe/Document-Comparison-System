from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey
)

from sqlalchemy.orm import relationship

from app.core.database import Base



class DocumentGroup(Base):

    __tablename__ = "document_groups"


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


    doc_type = Column(
        String,
        nullable=False
    )


    ref_hint = Column(
        String,
        nullable=True
    )


    confidence = Column(
        Float,
        nullable=False
    )


    pages = relationship(
        "DocumentGroupPage",
        back_populates="group"
    )