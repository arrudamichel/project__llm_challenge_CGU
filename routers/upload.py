from fastapi import APIRouter, UploadFile, File, Form
from typing import List
import tempfile
from services import pdf_loader, chunking, vector_database
import os 

router = APIRouter()

@router.post("/")
async def upload_docs(files: List[UploadFile] = File(...), chunk_size: int = Form(1000), chunk_overlap: int = Form(200)):
    files_name = []
    for file in files:
        content = await file.read()
        # Temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(content)
            tmp_file_path = tmp_file.name

        text = pdf_loader.load(tmp_file_path, file.filename)
        chunks = chunking.chunk_text(text, chunk_size, chunk_overlap)

        vector_database.save(chunks)
        
        files_name.append(file.filename)
        os.remove(tmp_file_path)

    return {"status": "success", "loaded_files": files_name}
