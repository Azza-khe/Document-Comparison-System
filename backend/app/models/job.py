from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base



class Job(Base):

    __tablename__ = "jobs"


    job_id = Column(
        String,
        primary_key=True
    )


    filename = Column(
        String,
        nullable=False
    )


    object_name = Column(
        String,
        nullable=False
    )


    status = Column(
        String,
        default="UPLOADED"
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


    pages = relationship(
        "Page",
        back_populates="job",
        cascade="all, delete"
    )