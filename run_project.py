# run_project.py
import sqlite3
from app import init_db, save_transcription

# 1️⃣ Initialize the database
init_db()

# 2️⃣ Add a test user
def add_test_user(name, email):
    conn = sqlite3.connect("transcribe.db")
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (name, email) VALUES (?, ?)", (name, email))
    conn.commit()
    # Get user_id of inserted user
    cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
    user_id = cursor.fetchone()[0]
    conn.close()
    return user_id

user_id = add_test_user("Test User", "test@example.com")
print(f"Test user added with user_id: {user_id}")

# 3️⃣ Test transcription
audio_file = "Test.mp3.mp3"  # Replace with your audio file
language = "en"  # or "kn" for Kannada

text = save_transcription(user_id, audio_file, language)
if text:
    print("Transcription saved successfully!")
    print("Transcribed text:", text)
else:
    print("Failed to transcribe audio.")
