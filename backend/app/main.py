from fastapi import FastAPI

app = FastAPI(
    title="Document Comparison System",
    version="1.0"
)


@app.get("/")
def home():
    return {
        "message": "Document Processing System is running"
    }