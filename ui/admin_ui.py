import streamlit as st
import sqlite3
from backend.database import DB_NAME
from backend.activity import log_activity


# ==================================================
# NAVIGATION BUTTONS
# ==================================================
def navigation_buttons():

    col1, col2 = st.sidebar.columns(2)

    if col1.button("🏠 Home", use_container_width=True):
        st.session_state.page = "role"
        st.session_state.user = None
        st.session_state.admin_logged = False
        st.rerun()

    if col2.button("🚪 Logout", use_container_width=True):
        st.session_state.admin_logged = False
        st.session_state.user = None
        st.session_state.page = "role"
        st.rerun()


# ==================================================
# ADMIN LOGIN
# ==================================================
def admin_login():

    st.title("🔐 Admin Login")

    admin_id = st.text_input("Admin ID", placeholder="A101")

    if st.button("Login"):

        if admin_id == "A101":
            st.session_state.admin_logged = True
            st.success("Admin Login Successful")
            st.rerun()
        else:
            st.error("Invalid Admin ID")


# ==================================================
# ADMIN DASHBOARD
# ==================================================
def admin_dashboard():

    st.sidebar.title("🏢 Admin Panel")

    navigation_buttons()

    menu = st.sidebar.radio(
        "Admin Controls",
        [
            "Dashboard",
            "Upload University Data",
            "Students",
            "Add Student",
            "Activity Monitor",
            "System Control"
        ]
    )

    conn = sqlite3.connect(DB_NAME)

    # ================= DASHBOARD =================
    if menu == "Dashboard":

        st.title("📊 University AI Dashboard")

        total_students = conn.execute(
            "SELECT COUNT(*) FROM users"
        ).fetchone()[0]

        total_activity = conn.execute(
            "SELECT COUNT(*) FROM activity_logs"
        ).fetchone()[0]

        col1, col2 = st.columns(2)

        col1.metric("👨‍🎓 Students", total_students)
        col2.metric("🤖 AI Activities", total_activity)

        st.success("System Running Normally")

    # ================= UPLOAD =================
    elif menu == "Upload University Data":

        st.header("📚 Upload Knowledge Base")

        file = st.file_uploader("Upload PDF", type="pdf")

        if file:

            with open("knowledge.pdf", "wb") as f:
                f.write(file.getbuffer())

            result = st.session_state.ai_engine.process_pdf(
                "knowledge.pdf"
            )

            log_activity("ADMIN", "Uploaded University Data")

            st.success(result)

    # ================= STUDENTS =================
    elif menu == "Students":

        st.header("👨‍🎓 Student Records")

        students = conn.execute("SELECT * FROM users").fetchall()

        st.dataframe(students, use_container_width=True)

    # ================= ADD STUDENT =================
    elif menu == "Add Student":

        st.header("➕ Add Student")

        reg = st.text_input("Registration ID")
        name = st.text_input("Name")
        branch = st.text_input("Branch")
        year = st.text_input("Year")
        sem = st.text_input("Semester")

        if st.button("Create Student"):

            conn.execute(
                "INSERT INTO users VALUES (?,?,?,?,?)",
                (reg, name, branch, year, sem)
            )

            conn.commit()

            log_activity("ADMIN", f"Added Student {name}")

            st.success("Student Added")

    # ================= ACTIVITY =================
    elif menu == "Activity Monitor":

        st.header("📈 Activity Logs")

        logs = conn.execute("""
            SELECT user, action, timestamp
            FROM activity_logs
            ORDER BY id DESC
        """).fetchall()

        st.dataframe(logs, use_container_width=True)

    # ================= SYSTEM CONTROL =================
    elif menu == "System Control":

        st.header("⚙️ Backend Controls")

        if st.button("Clear Activity Logs"):

            conn.execute("DELETE FROM activity_logs")
            conn.commit()

            log_activity("ADMIN", "Cleared Logs")

            st.success("Logs Cleared")

        if st.button("Reset Knowledge Base"):

            open("knowledge.pdf", "w").close()

            log_activity("ADMIN", "Reset Knowledge")

            st.success("Knowledge Reset")

    conn.close()


# ==================================================
# MAIN ADMIN UI
# ==================================================
def admin_ui():

    if "admin_logged" not in st.session_state:
        st.session_state.admin_logged = False

    if not st.session_state.admin_logged:
        admin_login()
    else:
        admin_dashboard()
