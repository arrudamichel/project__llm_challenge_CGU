from fastapi import APIRouter
from typing import Optional
from services import vector_database, llm_model
from rank_bm25 import BM25Okapi

router = APIRouter()

@router.get("/")
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
