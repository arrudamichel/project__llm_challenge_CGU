from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = Chroma(collection_name="cgu", persist_directory="chroma_db", embedding_function=embedding_model)


def save(chunks):
    vectorstore.add_documents(chunks)

def search(question, top_k=5):
    return vectorstore.similarity_search(question, k=top_k)

def search_by_filename(question, filename, top_k=5):
    return vectorstore.similarity_search(question, k=top_k, filter={"filename": filename})