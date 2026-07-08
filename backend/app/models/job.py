from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.core.database import Base



class Job(Base):

    __tablename__="jobs"


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



    pages = relationship(
        "Page",
        back_populates="job",
        cascade="all, delete"
    )