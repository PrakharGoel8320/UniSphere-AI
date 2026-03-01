import streamlit as st
from backend.auth import login_student, login_admin

def login_screen():

    st.title("🎓 University AI Platform")

    role = st.radio("Select Role", ["Student", "Admin"])

    if role == "Student":

        sid = st.text_input("Registration ID")

        if st.button("Login"):
            user = login_student(sid)
            st.session_state.user = sid
            st.session_state.role = "student"
            st.rerun()

    else:
        aid = st.text_input("Admin ID")
        pwd = st.text_input("Password", type="password")

        if st.button("Login Admin"):
            if login_admin(aid, pwd):
                st.session_state.user = aid
                st.session_state.role = "admin"
                st.rerun()
            else:
                st.error("Invalid admin credentials")
