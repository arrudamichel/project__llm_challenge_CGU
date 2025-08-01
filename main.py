from fastapi import FastAPI
from routers import upload, rag, classify
from starlette.middleware.cors import CORSMiddleware

app = FastAPI(title="CGU Data Scientist Challenge API", 
              docs_url="/docs", 
              redoc_url="/redoc")

app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(upload.router, prefix="/upload", tags=["Upload"])
app.include_router(rag.router, prefix="/rag", tags=["RAG"])
app.include_router(classify.router, prefix="/classify", tags=["Classification"])

@app.get("/")
def root():
    return {"message": "API para desafio CGU - Cientista de Dados"}
