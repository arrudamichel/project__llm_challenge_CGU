from fastapi import APIRouter, UploadFile, File, Form
from typing import List

router = APIRouter()

@router.post("/")
async def upload_docs(files: List[UploadFile] = File(...), chunk_size: int = Form(1000), chunk_overlap: int = Form(200)):


    return {"status": "success", "loaded_files": ["file_name_1.pdf", "file_name_2.pdf"]}
