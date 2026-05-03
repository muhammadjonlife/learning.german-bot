import sqlite3

conn = sqlite3.connect("db.sqlite3")
cursor = conn.cursor()

def init_db():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        correct INTEGER DEFAULT 0,
        total INTEGER DEFAULT 0,
        streak INTEGER DEFAULT 0
    )
    """)
    conn.commit()

def add_user(user_id):
    cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    conn.commit()

def update_stats(user_id, correct):
    if correct:
        cursor.execute("UPDATE users SET correct = correct+1, total = total+1 WHERE user_id=?", (user_id,))
    else:
        cursor.execute("UPDATE users SET total = total+1 WHERE user_id=?", (user_id,))
    conn.commit()

def update_streak(user_id):
    cursor.execute("UPDATE users SET streak = streak + 1 WHERE user_id=?", (user_id,))
    conn.commit()

def get_stats(user_id):
    cursor.execute("SELECT correct, total, streak FROM users WHERE user_id=?", (user_id,))
    return cursor.fetchone()