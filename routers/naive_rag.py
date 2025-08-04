from fastapi import APIRouter, HTTPException
from typing import Optional
from services import vector_database, llm_model
from rank_bm25 import BM25Okapi

router = APIRouter()

@router.get("/full-database")
def naive_rag(question: str, bm25: Optional[bool] = False):
    results = vector_database.search(question, top_k=5)
    corpus = [doc.page_content for doc in results]
    
    if bm25:
        tokenized_corpus = [doc.split() for doc in corpus]
        bm25_model = BM25Okapi(tokenized_corpus)
        tokenized_query = question.split()
        corpus = bm25_model.get_top_n(tokenized_query, corpus, n=3)

    resp = llm_model.answer_question(question, corpus)

    return {"answer": resp}

@router.get("/by-filename")
def naive_rag(question: str, filename : str = None, bm25: Optional[bool] = False):
    if filename:
        results = vector_database.search_by_filename(question, filename, top_k=5)
    else:
        raise HTTPException(status_code=400, detail="Empty Filename.")

    corpus = [doc.page_content for doc in results]
    
    if bm25:
        tokenized_corpus = [doc.split() for doc in corpus]
        bm25_model = BM25Okapi(tokenized_corpus)
        tokenized_query = question.split()
        corpus = bm25_model.get_top_n(tokenized_query, corpus, n=3)

    resp = llm_model.answer_question(question, corpus)

    return {"answer": resp}