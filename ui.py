import streamlit as st
import sqlite3

from backend.database import init_db, DB_NAME
from core.ai_engine import UniSphereAI

from ui.admin_ui import admin_ui
from ui.student_ui import student_ui


# ------------------------------------------------
# INIT DATABASE
# ------------------------------------------------
init_db()

# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------
st.set_page_config(
    page_title="UniSphere AI",
    layout="wide",
    page_icon="🎓"
)

# ------------------------------------------------
# SESSION STATE
# ------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = "role"

if "user" not in st.session_state:
    st.session_state.user = None

if "ai_engine" not in st.session_state:
    st.session_state.ai_engine = UniSphereAI()

if "ai_mode" not in st.session_state:
    st.session_state.ai_mode = "General AI"

if "messages" not in st.session_state:
    st.session_state.messages = []


# ------------------------------------------------
# AI MODE DIALOG
# ------------------------------------------------
@st.dialog("Choose AI Mode")
def choose_mode():

    mode = st.radio(
        "Select AI Mode",
        ["General AI", "Lecture Summarizer", "Study Planner"],
        index=["General AI","Lecture Summarizer","Study Planner"]
        .index(st.session_state.ai_mode)
    )

    if st.button("Apply Mode", use_container_width=True):
        st.session_state.ai_mode = mode
        st.rerun()


# ------------------------------------------------
# ROLE SELECTION
# ------------------------------------------------
def role_page():

    st.title("🚀 UniSphere AI")
    st.subheader("Autonomous University Intelligence System")

    col1, col2 = st.columns(2)

    if col1.button("🎓 I am a Student", use_container_width=True):
        st.session_state.page = "student_login"
        st.rerun()

    if col2.button("🏢 I am an Admin", use_container_width=True):
        st.session_state.page = "admin_login"
        st.rerun()


# ------------------------------------------------
# STUDENT LOGIN
# ------------------------------------------------
def student_login():

    st.header("🎓 Student Login")

    reg = st.text_input("Registration ID", placeholder="Try 101")

    if st.button("Login", use_container_width=True):

        conn = sqlite3.connect(DB_NAME)

        user = conn.execute(
            "SELECT * FROM users WHERE reg_id=?",
            (reg,)
        ).fetchone()

        conn.close()

        if user:
            st.session_state.user = user
            st.session_state.page = "student_dashboard"
            st.rerun()
        else:
            st.error("Invalid Registration ID")


# ------------------------------------------------
# ADMIN LOGIN
# ------------------------------------------------
def admin_login():

    st.header("🏢 Admin Login")

    admin_id = st.text_input("Admin ID", placeholder="Use A101")

    if st.button("Login", use_container_width=True):

        conn = sqlite3.connect(DB_NAME)

        admin = conn.execute(
            "SELECT * FROM admins WHERE admin_id=?",
            (admin_id,)
        ).fetchone()

        conn.close()

        if admin:
            st.session_state.user = admin
            st.session_state.page = "admin_dashboard"
            st.rerun()
        else:
            st.error("Invalid Admin ID")


# ------------------------------------------------
# ROUTER
# ------------------------------------------------
pages = {
    "role": role_page,
    "student_login": student_login,
    "admin_login": admin_login,
    "student_dashboard": student_ui,
    "admin_dashboard": admin_ui,
}

pages[st.session_state.page]()
