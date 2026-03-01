import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_ollama import ChatOllama
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS

def create_knowledge_base():
    docs = []

    for file in os.listdir("data/university_docs"):
        if file.endswith(".pdf"):
            loader = PyPDFLoader(f"data/university_docs/{file}")
            docs.extend(loader.load())

    db = Chroma.from_documents(
        docs,
        OllamaEmbeddings(model="llama3"),
        persist_directory="vectorstore"
    )

    db.persist()


def ask_question(query):
    db = Chroma(
        persist_directory="vectorstore",
        embedding_function=OllamaEmbeddings(model="llama3")
    )

    qa = RetrievalQA.from_chain_type(
        llm=ChatOllama(model="llama3", temperature=0.3),
        retriever=db.as_retriever()
    )

    return qa.run(query)