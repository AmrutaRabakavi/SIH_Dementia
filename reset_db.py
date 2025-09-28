# reset_db.py
import sqlite3

DB_NAME = "transcribe.db"

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# Drop old table if exists
cursor.execute("DROP TABLE IF EXISTS transcriptions")

# Recreate with name + email directly
cursor.execute("""
CREATE TABLE IF NOT EXISTS transcriptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    audio_file TEXT,
    transcription TEXT,
    score REAL,
    label TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()

print("✅ Database reset with name + email columns")
