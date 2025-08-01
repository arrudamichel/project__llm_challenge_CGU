from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_ollama import OllamaLLM
import os

LLAMA_MODEL = "llama3.1"
llm_llama = OllamaLLM(model=LLAMA_MODEL)

parser = JsonOutputParser()
prompt = PromptTemplate(
template="""
    Você é um especialista em análise de sentimentos. 
    Classifique o sentimento da frase abaixo como 'positivo', 'negativo' ou 'neutro', e forneça a probabilidade (em percentual) para cada uma dessas classes.
    Não precisa justificar. Retorna somente o JSON.
    Retorne no seguinte formato JSON:
    {{
        "sentimento": "<classificação final>",
        "probabilidades": [
            {{"classe": "positivo", "probabilidade": <valor entre 0 e 1>}},
            {{"classe": "negativo", "probabilidade": <valor entre 0 e 1>}},
            {{"classe": "neutro", "probabilidade": <valor entre 0 e 1>}}
        ]
    }}

    Frase: "{text}"
    """,
        input_variables=["text"],
        output_parser=parser,
    )


def classify_sentiment_openai(text: str, model="gpt-4o-mini", api_key="sua-api-key-aqui") -> dict:
    os.environ["OPENAI_API_KEY"] = api_key
    
    # Inicializa o LLM com logprobs ativado
    llm_openai = ChatOpenAI(model=model)
    
    chain = prompt | llm_openai | parser
    resposta = chain.invoke({"text": text})

    return resposta


def classify_sentiment_llama(text: str) -> dict:

    chain = prompt | llm_llama | parser
    resposta = chain.invoke({"text": text})

    return resposta