import sqlite3

def init_db():
    conn = sqlite3.connect("alerts.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT,
        message TEXT,
        latitude TEXT,
        longitude TEXT,
        date TEXT
    )
    """)

    conn.commit()
    conn.close()