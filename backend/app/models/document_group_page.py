from sqlalchemy import (
    Column,
    Integer,
    ForeignKey
)

from sqlalchemy.orm import relationship

from app.core.database import Base



class DocumentGroupPage(Base):

    __tablename__ = "document_group_pages"


    id = Column(
        Integer,
        primary_key=True
    )


    group_id = Column(
        Integer,
        ForeignKey(
            "document_groups.id"
        )
    )


    page_id = Column(
        Integer,
        ForeignKey(
            "pages.id"
        )
    )


    group = relationship(
        "DocumentGroup",
        back_populates="pages"
    )