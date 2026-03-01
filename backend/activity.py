import sqlite3
from backend.database import DB_NAME


def log_activity(user, action):

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute(
        "INSERT INTO activity_logs(user, action) VALUES (?,?)",
        (str(user), action)
    )

    conn.commit()
    conn.close()
