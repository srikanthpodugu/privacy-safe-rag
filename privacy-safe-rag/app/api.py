from fastapi import APIRouter, UploadFile, File

from engine.ingestor import PrivacyIngestor
from engine.vault.token_vault import TokenVault


router = APIRouter()

ingestor = PrivacyIngestor()

vault = TokenVault()

# ==========================================================
# FILE UPLOAD ENDPOINT
# ==========================================================
@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...)
):

    content = await file.read()

    result = ingestor.process_file(
        content=content,
        filename=file.filename
    )

    return result


# ==========================================================
# TOKEN RE-IDENTIFICATION
# ==========================================================
@router.get("/resolve/{token}")
def resolve_token(token: str):

    original_value = vault.resolve_token(token)

    return {
        "token": token,
        "original_value": original_value
    }