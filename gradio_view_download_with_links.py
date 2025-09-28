# gradio_view_download.py
import gradio as gr
import sqlite3
import pandas as pd

DB_NAME = "transcribe.db"

def get_transcriptions():
    """Fetch all transcriptions and return both HTML table and CSV file path."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT t.id, u.name, u.email, t.audio_file, t.transcription, t.language, t.created_at
        FROM transcriptions t
        JOIN users u ON t.user_id = u.id
        ORDER BY t.created_at DESC
    """)
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        html_table = "<p>No transcriptions found.</p>"
        return html_table, None

    # Build HTML table manually
    html = "<table border='1' style='border-collapse: collapse; width: 100%;'>"
    html += "<tr><th>ID</th><th>User Name</th><th>Email</th><th>Audio File</th><th>Transcription</th><th>Language</th><th>Created At</th></tr>"
    for row in rows:
        html += "<tr>" + "".join([f"<td>{col}</td>" for col in row]) + "</tr>"
    html += "</table>"

    # Save CSV for download
    df = pd.DataFrame(rows, columns=["ID", "User Name", "Email", "Audio File", "Transcription", "Language", "Created At"])
    csv_file = "transcriptions.csv"
    df.to_csv(csv_file, index=False, encoding='utf-8')

    return html, csv_file

iface = gr.Interface(
    fn=get_transcriptions,
    inputs=[],
    outputs=[gr.HTML(), gr.File(label="Download Table as CSV")],
    title="View & Download Transcriptions",
    description="Click 'Submit' to generate a clean table of all saved transcriptions and download it as a CSV file."
)

iface.launch()
