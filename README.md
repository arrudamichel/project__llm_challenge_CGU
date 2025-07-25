# Teste Cientista de Dados CGU

Deve ser construida uma API utilizando FastAPI com três endpoints principais, conforme
especificado abaixo.

- Upload de PDF: Receber arquivos, realizar o processamento de dados, criação de embeddnigs e indexação em banco vetorial
- naive-RAG: Receber uma pergunta e retornar a resposta adequada baseada nos documentos indexados.
- Classificador de sentimentos: Receber uma sentença e classificar usando LLM ou SLM. Preferencialmente, utilizar logprobs para fundamentar a classificação

## Arquivos de teste

Para testar os serviços de upload dos arquivos e de RAG para responder com base nesse contexto, foram "impressos" em PDF algumas páginas da web com definições sobre MLOps. A ideia é que o RAG consiga responder sobre esse assunto. Os arquivos estão disponíveis na pasta `pdfs_para_tests/`.

## Arquitetura proposta

![Arquitetura da API](images/arquitetura.png)

### API Gateway

O API Gateway é uma camada intermediária entre clientes e serviços de backend, centralizando a gestão de requisições e funções críticas como autenticação, autorização, rate limiting, roteamento e segurança. Ele atua como ponto único de entrada para todas as chamadas de API.

Vantagens:
  - Implementa OAuth2, JWT e Criptografia HTTPS, garantindo autenticação robusta e proteção dos dados em trânsito.

  - Configura rate limiting, prevenindo ataques DDoS e abusos de requisições.

  - Isola as camadas de aplicação e banco de dados, mantendo os serviços internos protegidos e ocultos do público. 


### Load Balancer

O Load Balancer distribui o tráfego de forma equilibrada entre múltiplos pods, servidores ou instâncias da aplicação, otimizando recursos e garantindo disponibilidade.

Vantagens:
- Evita sobrecarga em um único servidor, o que poderia comprometer o desempenho e causar indisponibilidades. 

- Facilita a escalabilidade horizontal, com adição ou remoção de instâncias de forma transparente para o cliente.

- Aumento da resiliência e disponibilidade. Caso uma instância falhe, o Load Balancer automaticamente redireciona as requisições para outros servidores saudáveis, garantindo a continuidade do serviço.

### Camada de aplicação:

#### API Layer 

A API Layer é o núcleo responsável por receber, processar e responder às requisições dos clientes. Nesta camada, a API (FastAPI) é executada em um cluster Kubernetes, distribuída em múltiplos pods para garantir alta escalabilidade, disponibilidade e tolerância a falhas.

Vantagens: 
- Capacidade de escalar horizontalmente, aumentando ou diminuindo a quantidade de pods automaticamente de acordo com a demanda.

- Cada pod pode aproveitar ao máximo os recursos da máquina que o hospeda ao utilizar múltiplos workers (de API), garantindo melhor desempenho no processamento das requisições.

- Suporte a processamento síncrono e assíncrono, com filas (Queue) para tarefas pesadas e assíncronas.


- Essa abordagem garante eficiência, alta performance e resiliência, além de possibilitar o escalonamento tanto de pods quanto de nós (máquinas) do cluster Kubernetes. Com isso, o sistema consegue lidar com grandes volumes de tráfego sem comprometer a qualidade do serviço.

#### Queue (Fila)

É responsável por gerenciar tarefas assíncronas que não precisam ser processadas imediatamente pela API, permitindo que operações mais pesadas sejam executadas em segundo plano por workers especializados. Ao intermediar a comunicação entre a camada de API e os workers, a fila garante que o sistema continue responsivo mesmo sob alta carga, evitando bloqueios e lentidão.

#### Workers

É composta por pods especializados e dedicados dentro do cluster Kubernets e são responsáveis por executar tarefas complexas e demoradas que são delegadas pela fila (Queue). São configurados com GPU própria para realizar a execução inferência de modelos LLM (Large Language Models).

Vantagens:

- Execução paralela de workloads pesadas (ex.: upload ou geração de respostas via LLM).

- Aproveitamento de GPU, acelerando inferências e tarefas de IA.

- Escalabilidade independente, ajustando a quantidade de workers sem afetar a API.


#### VectorDB

A camada de VectorDB é responsável por armazenar e gerenciar representações vetoriais (embeddings) de documentos, textos ou outros dados, permitindo buscas semânticas altamente eficientes e precisas. 

A ferramenta utilizada foi o ChromaDB, um banco de dados vetorial otimizado para operações de similaridade, essencial em aplicações que envolvem LLMs (Large Language Models) e RAG (Retrieval-Augmented Generation).

## Exemplo de Operação Assíncrona
![Upload Files](images/upload_files.png)

Neste exemplo, é ilustrado o fluxo de execução do serviço de upload de arquivos. Como o envio e o processamento dos arquivos podem ser operações pesadas e demoradas, foi adotado um fluxo assíncrono para manter a API sempre disponível. Assim, ao receber o arquivo, o endpoint de upload retorna uma resposta de sucesso (HTTP 200) confirmando o recebimento, enquanto a requisição é enviada para a fila de processamento.

A fila gerencia o momento adequado para iniciar o processamento, direcionando a tarefa para um worker especializado, responsável pelas etapas de chunkização, geração de embeddings e armazenamento no banco vetorial (VectorDB). Ao finalizar o processamento, a API é notificada por meio de um serviço de callback, informando a conclusão com sucesso.

## LLM, RAG e afins

- Biblioteca majoritariamente utilizada: `Langchain`

O LangChain foi escolhido por ser amplamente utilizado como biblioteca para aplicações RAG, fornecendo abstrações de alto nível que facilitam a construção de pipelines com LLMs, desde a preparação de dados (splitters e embeddings) até a orquestração de respostas oriundas do modelo LLM.

- Modelo LLM para responder questões: `llama3.1` usando a biblioteca `Ollama`.

O Llama 3.1 é amplamente utilizado e foi escolhido por ter custo zero por uso, podendo ser executado na máquina local e tento qualidade comparável a modelos pagos. Por ter execução local, garante menor latência e maior controle de dados sensíveis. Além disso, tem boa integração com a biblioteca usada para o RAG, o LangChain, a partir do uso do Ollama.

- Chuknização: `RecursiveCharacterTextSplitter`

Esse splitter é recomendado pela documentação do LangChain por ser flexível e otimizado para lidar com textos de diferentes tamanhos, respeitando limites de tokens do modelo. Ele divide os documentos em partes menores (chunks) de forma hierárquica, buscando preservar a estrutura semãntica, o que melhora a relevância dos chunks para uso na recuperação de informações (RAG). 

- Geração de embeddings: modelo `sentence-transformers/all-MiniLM-L6-v2`

Este modelo é amplamente utilizado no mercado gerando embeddings semânticos de alta qualidade com baixo custo computacional. É ideal para aplicações de RAG, pois mantém performance robusta mesmo em hardware limitado, podendo ser executado em máquina local.

- Banco vetorial: ChromaDB

O ChromaDB é o banco vetorial padrão do ecossistema LangChain, amplamente testado e documentado. Sua integração com LangChain garante facilidade de implementação, suporte para persistência local e velocidade na busca por dados.


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

- [TODO][POST] /classify/

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

## Referências para implementação

  - LLM e API
    
    Projeto pessoal para criação de chat que tem como objetivo responder sobre espiritismo a partir de livros de Allan Kardec carregados como contexto do RAG. 
  
    Link: https://github.com/arrudamichel/project__spiritism_chat

- API
  -  Projeto pessoal para criação de chat que tem como objetivo responder sobre espiritismo a partir de livros de Allan Kardec carregados como contexto do RAG. 
  
      Link: https://github.com/arrudamichel/project__spiritism_chat

  - Projeto de dissertação que auxiliei na elaboração de uma API com FastAPI para upload de imagens, processamento e retorno das emoções que as cores expressavam.
  
      Link: https://github.com/airinecarmo/api-emotion-colors-images

- BM25

  Dissertação de mestrado: Usei BM25 como baseline comparativo para as técnicas propostas na dissertação.

  Link: https://www.cos.ufrj.br/uploadfile/publicacao/2921.pdf