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

# === message_generator.py ===
def generate_message(mood_data):
    print(f"[INFO] Generating message for mood data: {mood_data}")
    if not mood_data:
        return "Goodnight my love ❤️ I hope today was gentle on your heart. Sleep peacefully."

    mood, note = mood_data
    if mood == "sad":
        return "I know today was hard 😔 but I'm here with you in spirit. Sleep easy, my heart."
    elif mood == "ok":
        return "Another day done. I'm proud of you, babe. Rest up 😌💤"
    elif mood == "happy":
        return "You're glowing brighter than the moon tonight ✨ Sweet dreams my love 💋"
    else:
        return f"Goodnight sweetheart ❤️ Today you felt: {mood}. I’m thinking of you always."
