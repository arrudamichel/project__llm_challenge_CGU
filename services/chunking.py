from langchain.text_splitter import RecursiveCharacterTextSplitter


def chunk_text(content, chunk_size=100, chunk_overlap=200):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    docs = splitter.split_documents(content)
    return docs
