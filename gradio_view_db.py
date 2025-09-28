# gradio_view_db.py
import gradio as gr
import sqlite3
import pandas as pd

DB_NAME = "transcribe.db"

def view_database():
    """Fetch all transcriptions and display as a clean table."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Join users and transcriptions
    cursor.execute("""
        SELECT t.id, u.name, u.email, t.audio_file, t.transcription, t.language, t.created_at
        FROM transcriptions t
        JOIN users u ON t.user_id = u.id
        ORDER BY t.created_at ASC
    """)
    rows = cursor.fetchall()
    conn.close()
    
    # Convert to DataFrame and remove index
    df = pd.DataFrame(rows, columns=["ID", "User Name", "Email", "Audio File", "Transcription", "Language", "Created At"])
    df.index = range(1, len(df)+1)  # optional: start numbering from 1
    return df

# Gradio interface
iface = gr.Interface(
    fn=view_database,
    inputs=[],  # no filters
    outputs="dataframe",
    title="View All Transcriptions",
    description="Click 'Submit' to generate a clean table of all saved transcriptions."
)

iface.launch()
