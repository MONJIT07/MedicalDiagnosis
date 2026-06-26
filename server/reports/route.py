from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from typing import List
import uuid

from ..auth.route import authenticate
from .vectorstore import load_vectorstore

router = APIRouter(
    prefix="/reports",
    tags=["reports"]
)


@router.post("/upload")
async def upload_reports(
    user=Depends(authenticate),
    files: List[UploadFile] = File(...)
):
    if user["role"] != "patient":
        raise HTTPException(
            status_code=403,
            detail="Only patients can upload reports."
        )

    uploaded_reports = []

    for file in files:

        doc_id = str(uuid.uuid4())

        await load_vectorstore(
            uploaded_files=[file],      # <-- THIS IS THE FIX
            uploaded=user["username"],
            doc_id=doc_id
        )

        uploaded_reports.append(
            {
                "filename": file.filename,
                "doc_id": doc_id
            }
        )

    return uploaded_reports