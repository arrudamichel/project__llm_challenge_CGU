from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser

llm = Ollama(model="llama3.1")


def answer_question(question, docs):
    docs_str = " ".join(docs)
    
    template = """
    Responda à pergunta somente com base no contexto. Responder sempre em português.
    Caso não ache a resposta, responda que não existe resposta no contexto.
    Context: {context}

    Question: {question}
    Answer:
    """

    prompt = PromptTemplate(template=template, input_variables=["context", "question"])

    rag_chain = (
        {"context": RunnableLambda(lambda _: docs_str), "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain.invoke(question)