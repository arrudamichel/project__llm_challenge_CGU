from fastapi import APIRouter, HTTPException
from typing import Optional
from services import rag

router = APIRouter()

@router.get("/full-database")
def naive_rag(question: str):
    results = rag.execute(question)
    return {"answer": results}

@router.get("/by-filename")
def naive_rag(question: str, filename: str):
    if filename:
        results = rag.execute(question, filename)
    else:
        raise HTTPException(status_code=400, detail="Empty Filename.")
    
    return {"answer": results}
