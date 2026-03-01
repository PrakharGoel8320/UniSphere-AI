# app.py

import streamlit as st
from ui.admin_ui import admin_ui
from ui.student_ui import student_ui

st.sidebar.title("Login As")

role = st.sidebar.radio(
    "Select Role",
    ["Student", "Admin"]
)

if role == "Student":
    student_ui()

else:
    admin_ui()
