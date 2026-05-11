from fastapi import APIRouter, UploadFile, File
from engine.ingestor import PrivacyIngestor

router = APIRouter()

ingestor = PrivacyIngestor()

# ==========================================================
# FILE UPLOAD ENDPOINT
# ==========================================================
@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    content = await file.read()

    result = ingestor.process_file(
        content=content,
        filename=file.filename
    )

    return {
        "filename": file.filename,
        "status": "processed",
        "output": result
    }