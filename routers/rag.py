from fastapi import APIRouter
from typing import Optional

router = APIRouter()

@router.get("/")
def naive_rag(question: str, bm25: Optional[bool] = False):
    return {"answer": "resposta"}
