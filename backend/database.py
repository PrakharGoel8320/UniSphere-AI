import sqlite3

DB_NAME = "unisphere.db"

universities = []
students = []
documents = []

def init_db():

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # ---------------- USERS  ----------------
    c.execute("""
    CREATE TABLE IF NOT EXISTS users(
        reg_id TEXT PRIMARY KEY,
        name TEXT,
        branch TEXT,
        year TEXT,
        semester TEXT
    )
    """)

    # ---------------- ADMINS  ----------------
    c.execute("""
    CREATE TABLE IF NOT EXISTS admins(
        admin_id TEXT PRIMARY KEY,
        name TEXT
    )
    """)

    # ---------------- ACTIVITY  LOGS ----------------
    c.execute("""
    CREATE TABLE IF NOT EXISTS activity_logs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT,
        action TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # ---------- DEFAULT STUDENT ----------
    c.execute("""
    INSERT OR IGNORE INTO users
    VALUES ('101','John Doe','CSE','3rd','6th')
    """)

    # ---------- DEFAULT ADMIN ----------
    c.execute("""
    INSERT OR IGNORE INTO admins
    VALUES ('A101','Super Admin')
    """)

    conn.commit()
    conn.close()
