import streamlit as st
from modules.chatbot import ask_ai
from backend.activity import log_activity

# ==================================================
# SESSION SAFETY
# ==================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "ai_mode" not in st.session_state:
    st.session_state.ai_mode = "General AI"


# ==================================================
# NAVIGATION BUTTONS
# ==================================================
def navigation_buttons():

    col1, col2 = st.sidebar.columns(2)

    # HOME
    if col1.button("🏠 Home", use_container_width=True):
        st.session_state.page = "role"
        st.session_state.user = None
        st.session_state.messages = []
        st.rerun()

    # LOGOUT
    if col2.button("🚪 Logout", use_container_width=True):
        st.session_state.user = None
        st.session_state.messages = []
        st.session_state.page = "role"
        st.rerun()


# ==================================================
# STUDENT UI
# ==================================================
def student_ui():

    user = st.session_state.user

    # ---------------- SIDEBAR ----------------
    st.sidebar.title("🎓 Student Panel")

    navigation_buttons()

    page = st.sidebar.radio(
        "Menu",
        ["AI Chat", "Lecture Summarizer", "Study Planner"]
    )

    st.sidebar.markdown("---")

    mode = st.sidebar.selectbox(
        "🧠 Select AI Mode",
        [
            "General AI",
            "Lecture Summarizer",
            "Study Planner",
            "University QA"
        ],
        index=[
            "General AI",
            "Lecture Summarizer",
            "Study Planner",
            "University QA"
        ].index(st.session_state.ai_mode)
    )

    st.session_state.ai_mode = mode

    st.sidebar.success(f"Logged in as: {user[1]}")

    # ---------------- HEADER ----------------
    st.title(f"👋 Welcome {user[1]}")
    st.caption("UniSphere AI — Autonomous University Assistant")

    # ==================================================
    # AI CHAT
    # ==================================================
    if page == "AI Chat":

        st.subheader("💬 UniSphere AI Chat")

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        prompt = st.chat_input("Ask UniSphere AI...")

        if prompt:

            log_activity(user[1], "Asked AI Question")

            st.session_state.messages.append(
                {"role": "user", "content": prompt}
            )

            with st.chat_message("assistant"):
                response = ask_ai(prompt, st.session_state.ai_mode)
                st.markdown(response)

            st.session_state.messages.append(
                {"role": "assistant", "content": response}
            )

    # ==================================================
    # LECTURE SUMMARIZER
    # ==================================================
    elif page == "Lecture Summarizer":

        st.subheader("📚 Lecture Summarizer")

        uploaded_file = st.file_uploader(
            "Upload Lecture Notes",
            type=["pdf", "txt"]
        )

        if uploaded_file:

            content = uploaded_file.read().decode(errors="ignore")

            log_activity(user[1], "Uploaded Lecture Notes")

            with st.spinner("Summarizing..."):
                summary = ask_ai(content, "Lecture Summarizer")

            st.success("✅ Summary Generated")
            st.markdown(summary)

    # ==================================================
    # STUDY PLANNER
    # ==================================================
    elif page == "Study Planner":

        st.subheader("🧠 Study Planner")

        goal = st.text_area(
            "Enter Study Goal",
            placeholder="Prepare semester exams in 30 days"
        )

        if st.button("Generate Study Plan"):

            if goal:

                log_activity(user[1], "Generated Study Plan")

                with st.spinner("Creating plan..."):
                    plan = ask_ai(goal, "Study Planner")

                st.success("✅ Study Plan Ready")
                st.markdown(plan)

            else:
                st.warning("Please enter a goal.")
