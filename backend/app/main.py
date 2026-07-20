from fastapi import FastAPI

from app.api import upload
from app.api import analysis
from app.api import extraction
from app.models.job import Job
from app.models.page import Page
from app.models.document_group import DocumentGroup
from app.models.document_group_page import DocumentGroupPage
from app.models.extracted_document import ExtractedDocument
from app.models.extracted_item import ExtractedItem
from app.models.review_queue import ReviewQueue


app = FastAPI(
    title="Document Processing System",
    version="1.0"
)


# Routes Layer 0
app.include_router(
    upload.router,
    prefix="/api"
)


# Routes Layer 1
app.include_router(
    analysis.router,
    prefix="/api"
)

app.include_router(
    extraction.router
)

@app.get("/")
def home():

    return {
        "message": "Document Processing API running"
    }