from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langgraph.graph import StateGraph, END
from typing import TypedDict, List
from . import vector_database

# ----- Models -----
generator_low = OllamaLLM(model="llama3.1", temperature=0.3)
generator_mid = OllamaLLM(model="llama3.1", temperature=0.7)
generator_high = OllamaLLM(model="llama3.1", temperature=0.9)
llm_evaluator = OllamaLLM(model="llama3.1", temperature=0)

vectorstore_obj = vector_database.get_vectorstore() 
retriever = vectorstore_obj.as_retriever()

# ----- DEFINIÇÃO DO ESTADO -----
class RAGState(TypedDict):
    question: str
    filename: str
    responses: List[str]
    best_response: str

def get_context(question, filename):
    if filename:
        docs = retriever.get_relevant_documents(
            question,
            filter={"filename": filename}
        )
    else:
        docs = retriever.get_relevant_documents(question)
    
    return "\n".join([doc.page_content for doc in docs[:3]])


# ----- GERADOR DE RESPOSTAS -----
def generate_responses(state: RAGState) -> RAGState:
    question = state["question"]
    filename = state["filename"]
    
    context = get_context(question, filename)

    prompt = PromptTemplate.from_template("""
    Você é um assistente com acesso ao seguinte contexto:

    {context}

    Responda a pergunta a seguir com base no contexto acima:

    Pergunta: {question}
    Resposta:
    """)

    # Gerar múltiplas respostas com variação via temperatura
    r1 = generator_low.invoke(prompt.format(question=question, context=context)).strip()
    r2 = generator_mid.invoke(prompt.format(question=question, context=context)).strip()
    r3 = generator_high.invoke(prompt.format(question=question, context=context)).strip()
    
    return {"question": question, "responses": [r1, r2, r3], "best_response": ""}

# ----- AVALIADOR DE RESPOSTAS -----
def evaluate_responses(state: RAGState) -> RAGState:
    question = state["question"]
    filename = state["filename"]
    r = state["responses"]

    context = get_context(question, filename)

    eval_prompt = PromptTemplate.from_template("""
    Você é um avaliador. Dada a pergunta, o contexto e três respostas, escolha a melhor com base em clareza, relevância e completude.

    Contexto: {context}
                                               
    Pergunta: {question}

    Respostas:
    1. {r1}
    2. {r2}
    3. {r3}

    Indique apenas o número da melhor resposta (1, 2 ou 3).
    """)

    output = llm_evaluator.invoke(eval_prompt.format(
        question=question, context=context, r1=r[0], r2=r[1], r3=r[2]
    ))

    # Extrai o número da melhor resposta (1, 2 ou 3)
    index = next((i for i in ['1', '2', '3'] if i in output), "1")
    best = r[int(index) - 1]

    return {**state, "best_response": best}

# ----- DEFINIÇÃO DO GRAFO -----
graph_builder = StateGraph(RAGState)

graph_builder.add_node("GenerateResponses", generate_responses)
graph_builder.add_node("EvaluateResponses", evaluate_responses)

graph_builder.set_entry_point("GenerateResponses")
graph_builder.add_edge("GenerateResponses", "EvaluateResponses")
graph_builder.add_edge("EvaluateResponses", END)

graph = graph_builder.compile()


def execute(question : str, filename : str = None):
    input = {"question": question, "filename": filename}
    result = graph.invoke(input)
    return result["best_response"]
