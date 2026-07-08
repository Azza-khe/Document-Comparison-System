from fastapi import FastAPI

from app.api import upload
from app.api import analysis

from app.core.database import Base, engine

# Import des modèles pour que SQLAlchemy les connaisse
import app.models.job
import app.models.page


# Création des tables
Base.metadata.create_all(
    bind=engine
)


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


@app.get("/")
def home():

    return {
        "message": "Document Processing API running"
    }