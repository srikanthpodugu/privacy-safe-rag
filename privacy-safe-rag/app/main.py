from fastapi import FastAPI
from app.api import router

app = FastAPI(
    title="Privacy Safe AI Gateway",
    version="1.0"
)

app.include_router(router)

@app.get("/")
def health():
    return {"status": "running"}
