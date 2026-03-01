import streamlit as st
import sqlite3
import os
from gtts import gTTS

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="UniSphere AI",
    layout="wide",
    page_icon="🏆"
)

# ---------------- SESSION STATE ----------------
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user' not in st.session_state:
    st.session_state.user = None
if 'ai_engine' not in st.session_state:
    st.session_state.ai_engine = None

# ---------------- AI IMPORTS (OLLAMA VERSION) ----------------
try:
    from langchain_community.vectorstores import Chroma
    from langchain_community.document_loaders import PyPDFLoader
    from langchain.text_splitter import CharacterTextSplitter
    from langchain.chains import RetrievalQA
    from langchain_ollama import OllamaEmbeddings, ChatOllama

    LIBRARIES_LOADED = True
except ImportError:
    LIBRARIES_LOADED = False

# ---------------- DATABASE ----------------
DB_NAME = "unisphere.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        reg_id TEXT PRIMARY KEY,
        name TEXT,
        role TEXT,
        branch TEXT,
        year TEXT,
        sem TEXT)
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS admissions (
        dept TEXT,
        contact TEXT,
        location TEXT)
    """)

    c.execute(
        "INSERT OR IGNORE INTO users VALUES ('101','John Doe','Student','Computer Science','3rd','6th')"
    )

    c.execute(
        "INSERT OR IGNORE INTO admissions VALUES ('Academic Cell','admin@uni.edu','Block A, Room 102')"
    )

    conn.commit()
    conn.close()

init_db()

# ---------------- AI ENGINE ----------------
class UniSphereAI:

    def __init__(self):

        # LOCAL LLM
        self.llm = ChatOllama(
            model="llama3",
            temperature=0.2
        )

        # LOCAL EMBEDDINGS
        self.embeddings = OllamaEmbeddings(
            model="llama3"
        )

        self.vector_db = None

    def process_pdf(self, file_path):

        try:
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

            return "✅ University Knowledge Base Created Locally!"

        except Exception as e:
            return f"❌ Error: {str(e)}"

    def ask_question(self, query):

        if not self.vector_db:
            return "Upload university documents first."

        qa = RetrievalQA.from_chain_type(
            llm=self.llm,
            retriever=self.vector_db.as_retriever()
        )

        return qa.run(query)


# Create AI engine once
if LIBRARIES_LOADED and st.session_state.ai_engine is None:
    st.session_state.ai_engine = UniSphereAI()

# ---------------- UI ----------------
if not LIBRARIES_LOADED:
    st.error(
        "Install required libraries:\n\npip install langchain langchain-community langchain-ollama chromadb"
    )
    st.stop()

# -------- STYLE --------
st.markdown("""
<style>
.stApp { background-color:#0e1117; color:white; }
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
with st.sidebar:

    st.title("🌐 UniSphere AI")
    st.write("Autonomous University Intelligence")
    st.markdown("---")

    if not st.session_state.logged_in:

        reg_id = st.text_input("Registration ID", placeholder="Try 101")

        if st.button("Enter Portal"):

            conn = sqlite3.connect(DB_NAME)
            user = conn.execute(
                "SELECT * FROM users WHERE reg_id=?",
                (reg_id,)
            ).fetchone()
            conn.close()

            if user:
                st.session_state.logged_in = True
                st.session_state.user = user
                st.rerun()
            else:
                st.error("Invalid ID")

    else:

        st.success(f"Logged in as {st.session_state.user[1]}")

        menu = st.radio(
            "Navigation",
            ["Dashboard", "University Admin", "Admission Assistant", "Future Proxy"]
        )

        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

# ---------------- MAIN ----------------
if not st.session_state.logged_in:

    st.title("Welcome to UniSphere AI")

    st.markdown("""
### 🚀 Local University AI Assistant

✅ Works Offline  
✅ Private Student Data  
✅ Local LLM Powered by Ollama  
✅ Ryzen AI Ready

Login using Student ID.
""")

else:

    user = st.session_state.user

    if menu == "Dashboard":

        st.header(f"🎓 Dashboard — {user[1]}")

        query = st.text_input(
            "Ask about timetable, exams, syllabus:"
        )

        if query:
            with st.spinner("Thinking locally..."):
                answer = st.session_state.ai_engine.ask_question(query)
                st.success(answer)

        st.divider()

        st.write("**Branch:**", user[3])
        st.write("**Year:**", user[4])
        st.write("**Semester:**", user[5])

    elif menu == "University Admin":

        st.header("🏢 Upload University Documents")

        file = st.file_uploader("Upload PDF", type="pdf")

        if file:

            with open("temp.pdf", "wb") as f:
                f.write(file.getbuffer())

            with st.spinner("Training AI Brain..."):
                result = st.session_state.ai_engine.process_pdf("temp.pdf")

            st.success(result)

    elif menu == "Admission Assistant":

        st.header("🏫 Admission Assistant")

        q = st.text_input("Ask admission question")

        if q:
            conn = sqlite3.connect(DB_NAME)
            contact = conn.execute("SELECT * FROM admissions").fetchone()
            conn.close()

            st.json({
                "Department": contact[0],
                "Email": contact[1],
                "Office": contact[2]
            })

    elif menu == "Future Proxy":

        st.header("🤖 AI Meeting Proxy")

        st.info(
            "Future feature: AI attends meeting and gives summary automatically."
        )

        st.progress(40)
