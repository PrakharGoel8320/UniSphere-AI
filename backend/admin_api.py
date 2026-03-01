# backend/admin_api.py

from backend.database import universities, students, documents


# ======================
# ADMIN LOGIN
# ======================

def admin_login(admin_id):

    # Fake Admin
    if admin_id == "A101":
        return True

    return False


# ======================
# UNIVERSITY MANAGEMENT
# ======================

def add_university(name, location):

    universities.append({
        "name": name,
        "location": location
    })


def get_universities():
    return universities


def delete_university(index):
    if index < len(universities):
        universities.pop(index)


# ======================
# STUDENT MANAGEMENT
# ======================

def get_students():
    return students


# ======================
# DOCUMENT MANAGEMENT
# ======================

def upload_document(student, title):

    documents.append({
        "student": student,
        "title": title,
        "verified": False
    })


def get_documents():
    return documents


def verify_document(index):
    if index < len(documents):
        documents[index]["verified"] = True
