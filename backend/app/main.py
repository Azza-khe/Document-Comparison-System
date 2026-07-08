from fastapi import FastAPI

from app.api import upload
from app.core.database import Base
from app.core.database import engine

import app.models.job

Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="Document Processing System",
    version="1.0"
)


app.include_router(
    upload.router,
    prefix="/api"
)


@app.get("/")
def home():

    return {
        "message":
        "Document Processing API running"
    }