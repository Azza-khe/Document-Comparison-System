from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    DateTime
)

from datetime import datetime

from app.core.database import Base



class ReviewQueue(Base):

    __tablename__ = "review_queue"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    page_id = Column(
        Integer,
        nullable=False
    )


    document_type = Column(
        String,
        default="UNKNOWN"
    )


    confidence = Column(
        Float,
        default=0.0
    )


    status = Column(
        String,
        default="PENDING"
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


    resolved = Column(
        Boolean,
        default=False
    )