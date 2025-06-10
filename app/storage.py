import sqlite3

def init_db():
    conn = sqlite3.connect("resumes.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS resumes (
            id INTEGER PRIMARY KEY,
            name TEXT, email TEXT, phone TEXT,
            skills TEXT, experience TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_data(data):
    conn = sqlite3.connect("resumes.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO resumes (name, email, phone, skills, experience) VALUES (?, ?, ?, ?, ?)",
                (data['name'], data['email'], data['phone'], ", ".join(data['skills']), data['experience']))
    conn.commit()
    conn.close()

def get_all_data():
    conn = sqlite3.connect("resumes.db")
    cur = conn.cursor()
    cur.execute("SELECT name, email, phone, skills, experience FROM resumes")
    rows = cur.fetchall()
    conn.close()
    return rows

init_db()
