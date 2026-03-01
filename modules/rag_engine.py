import os
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_ollama import ChatOllama
from langchain.chains import RetrievalQA

DB_PATH = "data/vector_db"


class RAGEngine:

    def __init__(self):

        self.embeddings = OllamaEmbeddings(
            model="llama3"
        )

        self.llm = ChatOllama(
            model="llama3",
            temperature=0
        )

        self.vector_db = None

        # Load existing DB if exists
        if os.path.exists(DB_PATH):
            self.vector_db = Chroma(
                persist_directory=DB_PATH,
                embedding_function=self.embeddings
            )

    # ---------------------------
    # ADMIN: Process University PDF
    # ---------------------------
    def ingest_pdf(self, pdf_path):

        loader = PyPDFLoader(pdf_path)
        documents = loader.load()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=150
        )

        docs = splitter.split_documents(documents)

        self.vector_db = Chroma.from_documents(
            docs,
            self.embeddings,
            persist_directory=DB_PATH
        )

        self.vector_db.persist()

        return "✅ University Knowledge Base Updated"

    # ---------------------------
    # STUDENT QUERY
    # ---------------------------
    def query(self, question):

        if not self.vector_db:
            return "⚠ No university knowledge uploaded yet."

        qa = RetrievalQA.from_chain_type(
            llm=self.llm,
            retriever=self.vector_db.as_retriever(),
            chain_type="stuff"
        )

        return qa.run(question)
