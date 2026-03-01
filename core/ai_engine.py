import os
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter

DB_NAME = "unisphere.db"


class UniSphereAI:

    def __init__(self):

        self.llm = ChatOllama(
            model="llama3",
            temperature=0
        )

        self.embeddings = OllamaEmbeddings(
            model="llama3"
        )

        self.vector_db = None

    def process_pdf(self, file_path):

        loader = PyPDFLoader(file_path)
        documents = loader.load()

        splitter = CharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100
        )

        docs = splitter.split_documents(documents)

        self.vector_db = Chroma.from_documents(
            docs,
            self.embeddings,
            persist_directory="vectorstore"
        )

        return "✅ Knowledge Base Updated"

    def ask_question(self, query):

        if not self.vector_db:
            return "Upload university data first."

        qa = RetrievalQA.from_chain_type(
            llm=self.llm,
            retriever=self.vector_db.as_retriever()
        )

        return qa.run(query)
