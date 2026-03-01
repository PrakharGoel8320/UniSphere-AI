from backend.database import load_json, save_json

FAKE_ADMINS = {
    "A101": "admin123"
}

def login_student(student_id):
    students = load_json("students.json")

    if student_id not in students:
        students[student_id] = {
            "name": f"Student {student_id}",
            "active": True,
            "queries": 0
        }
        save_json("students.json", students)

    return students[student_id]


def login_admin(admin_id, password):
    return FAKE_ADMINS.get(admin_id) == password
