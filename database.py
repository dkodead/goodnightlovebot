import sqlite3

def init_db():
    print("[INFO] Initializing database...")
    conn = sqlite3.connect("moods.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS moods (
            date TEXT PRIMARY KEY,
            mood TEXT,
            note TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS context_log (
            timestamp TEXT,
            context TEXT
        )
    """)
    conn.commit()
    conn.close()
    print("[INFO] Database initialized.")

def save_mood(date, mood, note):
    print(f"[INFO] Saving mood to DB: {date}, {mood}, {note}")
    conn = sqlite3.connect("moods.db")
    c = conn.cursor()
    c.execute("REPLACE INTO moods (date, mood, note) VALUES (?, ?, ?)", (str(date), mood, note))
    conn.commit()
    conn.close()
    print("[INFO] Mood saved.")

def get_today_mood(date):
    print(f"[INFO] Fetching mood for date: {date}")
    conn = sqlite3.connect("moods.db")
    c = conn.cursor()
    c.execute("SELECT mood, note FROM moods WHERE date = ?", (str(date),))
    result = c.fetchone()
    conn.close()
    print(f"[INFO] Fetched mood result: {result}")
    return result

def save_context(context):
    from datetime import datetime
    print(f"[INFO] Saving context: {context}")
    conn = sqlite3.connect("moods.db")
    c = conn.cursor()
    c.execute("REPLACE INTO settings (key, value) VALUES (?, ?)", ("context", context))
    c.execute("INSERT INTO context_log (timestamp, context) VALUES (?, ?)", (datetime.now().isoformat(), context))
    conn.commit()
    conn.close()
    print("[INFO] Context saved and logged.")

def get_context():
    print("[INFO] Retrieving stored context...")
    conn = sqlite3.connect("moods.db")
    c = conn.cursor()
    c.execute("SELECT value FROM settings WHERE key = ?", ("context",))
    result = c.fetchone()
    conn.close()
    context_value = result[0] if result else None
    print(f"[INFO] Stored context: {context_value}")
    return context_value
