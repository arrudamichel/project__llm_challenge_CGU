# Teste Cientista de Dados CGU

Deve ser construida uma API utilizando FastAPI com três endpoints principais, conforme
especificado abaixo.

- Upload de PDF: Receber arquivos, realizar o processamento de dados, criação de embeddnigs e indexação em banco vetorial
- naive-RAG: Receber uma pergunta e retornar a resposta adequada baseada nos documentos indexados.
- Classificador de sentimentos: Receber uma sentença e classificar usando LLM ou SLM. Preferencialmente, utilizar logprobs para fundamentar a classificação

## Arquitetura proposta


## LLM, RAG e afins

- Para chuknização foi utilizado o `RecursiveCharacterTextSplitter` do Langchain para dividir o texto em chunks (tokens).
- Para embeddings foi utilizado o modelo `sentence-transformers/all-MiniLM-L6-v2`
- Para banco vetorial foi utilizado o ChromaDB que é padrão da documentação do Langchain. 

## API 

API com três serviços diferentes detalhados abaixo:

Serviços:

- [POST] /upload/

Serviço para upload de arquivos .pdf, chunknização, geração de embeddings e armazenamento vetorial. Além dos arquivos .pdf de entrada, o serviço recebe parametros para configuração da chunknização.

Parametros:
   
    - files: array<string> (required)
    - chunk_size: integer
    - chunk_overlap: integer

Resposta [200]:

```
{
  "status": "success",
  "loaded_files": [
    "file_name_1.pdf",
    "file_name_2.pdf"
  ]
}
```

- [GET] /rag/

Parametros:
   
    - question: string (required)
    - bm25: boolean

Resposta [200]:

```
{
  "answer": "resposta"
}
```

- [POST] /classify/

Parametros:
   
    - input_data: string (required)

Resposta [200]:

```
{
  "classification": "positive",
  "probability": 0.8
}
```


## Instalação e execução da API

Para instalar e executar o ambiente criado.
```
conda env create -f environment.yaml
conda activate test_cd_cgu
```

Para executar a API
```
uvicorn main:app --port 8080 --workers 4 
```

Para acesssar a documentação Swagger criada automaticamente pelo FastAPI:

```
http://localhost:8080/docs
```

Nessa documentação poderão ser realizados testes de execução da API