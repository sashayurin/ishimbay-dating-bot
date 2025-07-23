import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS profiles (
    user_id INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER,
    gender TEXT,
    photo TEXT,
    status TEXT,
    code INTEGER
)''')
conn.commit()

def save_profile(user_id, name, age, gender, photo, status, code):
    cursor.execute("REPLACE INTO profiles VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (user_id, name, age, gender, photo, status, code))
    conn.commit()

def get_pending_profiles():
    cursor.execute("SELECT user_id, name, age, gender, status, code, photo FROM profiles WHERE status IN ('pending_payment', 'pending_video')")
    return cursor.fetchall()

def approve_profile(user_id):
    cursor.execute("UPDATE profiles SET status = 'approved' WHERE user_id = ?", (user_id,))
    conn.commit()

def reject_profile(user_id):
    cursor.execute("DELETE FROM profiles WHERE user_id = ?", (user_id,))
    conn.commit()
