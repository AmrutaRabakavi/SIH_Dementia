# import gradio as gr
# import whisper

# # Load Whisper model
# whisper_model = whisper.load_model("base")

# # Function to transcribe audio
# def transcribe(audio):
#     if isinstance(audio, tuple):
#         # Gradio sometimes returns (sample_rate, data), we need the file path
#         audio_file = audio[0]  # take the path if available
#     else:
#         audio_file = audio

#     result = whisper_model.transcribe(audio_file)
#     return result["text"]

# # Gradio interface
# demo = gr.Interface(
#     fn=transcribe,
#     inputs=gr.Audio(label="Record your voice", type="filepath"),  # type="filepath" ensures Whisper can read it
#     outputs=gr.Textbox(label="Transcription")
# )

# demo.launch(share=True)



# import gradio as gr
# import whisper
# import librosa

# # Load the small model (faster than medium/large)
# whisper_model = whisper.load_model("small")

# def transcribe(audio_file):
#     if audio_file is None:
#         return "No audio provided."

#     # Load audio using librosa
#     audio, sr = librosa.load(audio_file, sr=16000)  # resample to 16kHz
#     result = whisper_model.transcribe(audio_file, fp16=False)
#     return result["text"]

# # Gradio UI
# with gr.Blocks() as demo:
#     gr.Markdown("## 🎙️ Multilingual Dementia Speech Transcriber")
#     gr.Markdown("Speak in Hindi, Marathi, Kannada, or English, and get real-time transcription.")

#     with gr.Row():
#         audio_input = gr.Audio(
#             label="Record your voice",
#             type="filepath"   # saves audio file and passes path to transcribe()
#         )
#         output_text = gr.Textbox(label="Transcription")

#     submit_btn = gr.Button("Submit")
#     submit_btn.click(fn=transcribe, inputs=audio_input, outputs=output_text)

# demo.launch()




# import gradio as gr
# import whisper

# # Load small/ base model for faster transcription
# whisper_model = whisper.load_model("base")

# # Map full language names to Whisper language codes
# LANGUAGE_MAP = {
#     "Hindi": "hi",
#     "Marathi": "mr",
#     "Kannada": "kn",
#     "English": "en"
# }

# def transcribe(audio_file, language_name):
#     # Convert language name to code
#     language_code = LANGUAGE_MAP[language_name]
    
#     # Transcribe with selected language
#     result = whisper_model.transcribe(audio_file, language=language_code)
#     return result["text"]

# # Gradio UI
# with gr.Blocks() as demo:
#     gr.Markdown("## 🎙️ Multilingual Dementia Speech Transcriber")
#     gr.Markdown("Select a language and speak in Hindi, Marathi, Kannada, or English for fast transcription.")

#     with gr.Row():
#         audio_input = gr.Audio(label="🎤 Record / Upload Audio", type="filepath")
#         language_choice = gr.Dropdown(
#             ["Hindi", "Marathi", "Kannada", "English"], value="English", label="Select Language"
#         )

#     output_text = gr.Textbox(label="📝 Transcription", lines=5)

#     transcribe_button = gr.Button("Transcribe")

#     transcribe_button.click(fn=transcribe, inputs=[audio_input, language_choice], outputs=output_text)

# demo.launch()


# app.py
# app.py
# import sqlite3
# from transcribe import transcribe_audio  # import transcription function
# from datetime import datetime

# DB_NAME = "transcribe.db"  # Database file

# def get_connection():
#     """Create and return a database connection."""
#     conn = sqlite3.connect(DB_NAME)
#     return conn

# def init_db():
#     """Initialize the database tables safely."""
#     conn = get_connection()
#     cursor = conn.cursor()

#     # Users table
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS users (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             name TEXT NOT NULL,
#             email TEXT UNIQUE NOT NULL
#         )
#     """)

#     # Transcriptions table
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS transcriptions (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             user_id INTEGER NOT NULL,
#             audio_file TEXT NOT NULL,
#             transcription TEXT,
#             language TEXT,
#             created_at TEXT DEFAULT CURRENT_TIMESTAMP,
#             FOREIGN KEY (user_id) REFERENCES users(id)
#         )
#     """)

#     conn.commit()
#     conn.close()
#     print(f"Database '{DB_NAME}' initialized successfully!")

# def save_transcription(user_id, audio_file_path, language=None):
#     """Transcribe audio and save the result into the database."""
#     text = transcribe_audio(audio_file_path, language)
#     if text is None:
#         return None

#     conn = get_connection()
#     cursor = conn.cursor()
#     cursor.execute("""
#         INSERT INTO transcriptions (user_id, audio_file, transcription, language, created_at)
#         VALUES (?, ?, ?, ?, ?)
#     """, (user_id, audio_file_path, text, language, datetime.now()))
#     conn.commit()
#     conn.close()
#     return text

# # Optional: run init_db automatically if this file is executed directly
# if __name__ == "__main__":
#     init_db()
#     # Example usage
#     # user_id = 1
#     # transcription = save_transcription(user_id, "example_audio.wav", language="en")
#     # print("Saved transcription:", transcription)


# app.py


# import sqlite3
# from transcribe import transcribe_audio
# from datetime import datetime

# DB_NAME = "transcribe.db"

# def get_connection():
#     """Create and return a database connection."""
#     conn = sqlite3.connect(DB_NAME)
#     return conn

# def init_db():
#     """Initialize the database tables safely."""
#     conn = get_connection()
#     cursor = conn.cursor()

#     # Users table
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS users (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             name TEXT NOT NULL,
#             email TEXT UNIQUE NOT NULL
#         )
#     """)

#     # Transcriptions table
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS transcriptions (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             user_id INTEGER NOT NULL,
#             audio_file TEXT NOT NULL,
#             transcription TEXT,
#             language TEXT,
#             created_at TEXT DEFAULT CURRENT_TIMESTAMP,
#             FOREIGN KEY (user_id) REFERENCES users(id)
#         )
#     """)

#     conn.commit()
#     conn.close()
#     print(f"Database '{DB_NAME}' initialized successfully!")

# def add_test_user(name, email):
#     """Add a user if not exists and return user_id."""
#     conn = get_connection()
#     cursor = conn.cursor()
#     cursor.execute("INSERT OR IGNORE INTO users (name, email) VALUES (?, ?)", (name, email))
#     conn.commit()
#     cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
#     user_id = cursor.fetchone()[0]
#     conn.close()
#     return user_id

# def save_transcription(user_id, audio_file_path, language=None):
#     """Transcribe audio and save the result into the database."""
#     text = transcribe_audio(audio_file_path, language)
#     if text is None:
#         return None

#     conn = get_connection()
#     cursor = conn.cursor()
#     cursor.execute("""
#         INSERT INTO transcriptions (user_id, audio_file, transcription, language, created_at)
#         VALUES (?, ?, ?, ?, ?)
#     """, (user_id, audio_file_path, text, language, datetime.now()))
#     conn.commit()
#     conn.close()
#     return text

# # Optional: run init_db automatically if executed directly
# if __name__ == "__main__":
#     init_db()



# app.py


# import sqlite3
# import os
# from heuristic_model import analyze_dementia

# DB_NAME = "transcribe.db"

# # ---------------- Database Initialization ---------------- #
# def init_db():
#     conn = sqlite3.connect(DB_NAME)
#     cursor = conn.cursor()
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS transcriptions (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             user_id INTEGER,
#             audio_file TEXT,
#             transcription TEXT,
#             language TEXT,
#             dementia_score REAL,
#             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#         )
#     """)
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS users (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             name TEXT,
#             email TEXT
#         )
#     """)
#     conn.commit()
#     conn.close()

# # ---------------- User Functions ---------------- #
# def add_test_user(name, email):
#     """Add user if not exists, return user_id."""
#     conn = sqlite3.connect(DB_NAME)
#     cursor = conn.cursor()
#     cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
#     row = cursor.fetchone()
#     if row:
#         user_id = row[0]
#     else:
#         cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
#         user_id = cursor.lastrowid
#         conn.commit()
#     conn.close()
#     return user_id

# # ---------------- Transcription Functions ---------------- #
# def transcribe_audio(file_path, language="en"):
#     """
#     Transcribe audio using your Whisper model or any logic.
#     For demo, returning dummy text.
#     Replace with your actual transcription logic.
#     """
#     return "This is a sample transcription of the uploaded audio."

# def save_transcription(user_id, file_path, language="en"):
#     """
#     Save transcription and compute dementia score.
#     Returns the transcribed text.
#     """
#     # 1. Transcribe audio
#     text = transcribe_audio(file_path, language)
#     if not text:
#         return None

#     # 2. Compute dementia score
#     score = analyze_dementia(text)

#     # 3. Save to DB
#     conn = sqlite3.connect(DB_NAME)
#     cursor = conn.cursor()
#     cursor.execute("""
#         INSERT INTO transcriptions (user_id, audio_file, transcription, language, dementia_score)
#         VALUES (?, ?, ?, ?, ?)
#     """, (user_id, file_path, text, language, score))
#     conn.commit()
#     conn.close()

#     return text

# def get_connection():
#     return sqlite3.connect(DB_NAME)


# import sqlite3
# import whisper
# import os
# from datetime import datetime
# from heuristic_model import analyze_dementia

# DB_NAME = "transcribe.db"

# # Load Whisper model
# whisper_model = whisper.load_model("base")

# # ---------------- Database ---------------- #
# def get_connection():
#     return sqlite3.connect(DB_NAME)

# def init_db():
#     """Initialize the database with users and transcriptions tables."""
#     conn = get_connection()
#     cursor = conn.cursor()

#     # Create users table
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS users (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             name TEXT NOT NULL,
#             email TEXT NOT NULL UNIQUE
#         )
#     """)

#     # Create transcriptions table with dementia_score + risk_label
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS transcriptions (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             user_id INTEGER,
#             audio_file TEXT,
#             transcription TEXT,
#             language TEXT,
#             dementia_score REAL,
#             risk_label TEXT,
#             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#             FOREIGN KEY (user_id) REFERENCES users (id)
#         )
#     """)

#     conn.commit()
#     conn.close()
#     print(f"Database '{DB_NAME}' initialized successfully!")

# # ---------------- User Management ---------------- #
# def add_test_user(name, email):
#     """
#     Insert a new user if not already exists, return user_id.
#     """
#     conn = get_connection()
#     cursor = conn.cursor()

#     cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
#     row = cursor.fetchone()

#     if row:
#         user_id = row[0]
#     else:
#         cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
#         user_id = cursor.lastrowid
#         conn.commit()

#     conn.close()
#     return user_id

# # ---------------- Transcription ---------------- #
# def transcribe_audio(file_path, language="en"):
#     """
#     Run Whisper transcription on audio file.
#     """
#     result = whisper_model.transcribe(file_path, language=language)
#     return result["text"]

# def save_transcription(user_id, file_path, language="en"):
#     """
#     Simple transcription save (without dementia risk).
#     """
#     text = transcribe_audio(file_path, language)
#     if not text:
#         return None

#     conn = get_connection()
#     cursor = conn.cursor()
#     cursor.execute("""
#         INSERT INTO transcriptions (user_id, audio_file, transcription, language, dementia_score, risk_label, created_at)
#         VALUES (?, ?, ?, ?, ?, ?, ?)
#     """, (user_id, os.path.basename(file_path), text, language, None, None, datetime.now()))
#     conn.commit()
#     conn.close()

#     return text

# def insert_transcription(name, email, audio_file, transcription, score, risk_label, language="en"):
#     """
#     Insert a transcription with dementia risk analysis into the DB.
#     """
#     # Get or create user_id
#     user_id = add_test_user(name, email)

#     conn = get_connection()
#     cursor = conn.cursor()
#     cursor.execute("""
#         INSERT INTO transcriptions (user_id, audio_file, transcription, language, dementia_score, risk_label, created_at)
#         VALUES (?, ?, ?, ?, ?, ?, ?)
#     """, (user_id, os.path.basename(audio_file), transcription, language, score, risk_label, datetime.now()))
#     conn.commit()
#     conn.close()


# app.py
import sqlite3
from datetime import datetime

DB_NAME = "transcribe.db"

def init_db():
    """Initialize database with only patient records (no user_id)."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transcriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            audio_file TEXT,
            transcription TEXT,
            score REAL,
            label TEXT,
            language TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def insert_transcription(name, email, audio_file, transcription, score, label):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO transcriptions (name, email, audio_file, transcription, score, label)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, email, audio_file, transcription, score, label))
    conn.commit()
    conn.close()
