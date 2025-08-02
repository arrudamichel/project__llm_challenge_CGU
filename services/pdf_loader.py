from langchain_community.document_loaders import PyPDFLoader


def load(tmp_file_path, file_name):
    loader = PyPDFLoader(tmp_file_path)
    docs = loader.load() 

    for d in docs:
        d.metadata.update({
            "filename": file_name,
            "page": d.metadata.get("page", None)
        })

    return docs