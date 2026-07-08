from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime

from datetime import datetime

from app.core.database import Base


class Job(Base):

    __tablename__ = "jobs"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    job_id = Column(
        String,
        unique=True,
        nullable=False
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
        default="RECEIVED"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )