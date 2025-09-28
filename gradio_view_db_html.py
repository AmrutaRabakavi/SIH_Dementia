# # gradio_view_db_html.py
# import gradio as gr
# import sqlite3
# import pandas as pd

# DB_NAME = "transcribe.db"

# def view_database_html():
#     """Fetch all transcriptions and return as an HTML table (no Gradio pagination/buttons)."""
#     conn = sqlite3.connect(DB_NAME)
#     cursor = conn.cursor()
#     cursor.execute("""
#         SELECT t.id, u.name, u.email, t.audio_file, t.transcription, t.language, t.created_at
#         FROM transcriptions t
#         JOIN users u ON t.user_id = u.id
#         ORDER BY t.created_at DESC
#     """)
#     rows = cursor.fetchall()
#     conn.close()

#     df = pd.DataFrame(rows, columns=["ID", "User Name", "Email", "Audio File", "Transcription", "Language", "Created At"])
#     if df.empty:
#         return "<p>No transcriptions found.</p>"

#     # Convert DataFrame to HTML table
#     html_table = df.to_html(index=False, escape=False)
#     return html_table

# # Gradio interface
# iface = gr.Interface(
#     fn=view_database_html,
#     inputs=[],  # no inputs
#     outputs=gr.HTML(),  # render HTML directly
#     title="View All Transcriptions",
#     description="Click 'Submit' to generate a clean table of all saved transcriptions."
# )

# iface.launch()





# # gradio_view_db_html.py
# import gradio as gr
# import sqlite3
# import pandas as pd

# DB_NAME = "transcribe.db"

# def view_database_html():
#     """Fetch all transcriptions and return as an HTML table (with Name + Email)."""
#     conn = sqlite3.connect(DB_NAME)
#     cursor = conn.cursor()
#     cursor.execute("""
#         SELECT u.name, u.email, t.audio_file, t.transcription, t.language, t.created_at
#         FROM transcriptions t
#         JOIN users u ON t.user_id = u.id
#         ORDER BY t.created_at DESC
#     """)
#     rows = cursor.fetchall()
#     conn.close()

#     df = pd.DataFrame(
#         rows,
#         columns=["User Name", "Email", "Audio File", "Transcription", "Language", "Created At"]
#     )
#     if df.empty:
#         return "<p>No transcriptions found.</p>"

#     # Convert DataFrame to HTML table
#     html_table = df.to_html(index=False, escape=False)
#     return html_table

# # Gradio interface
# iface = gr.Interface(
#     fn=view_database_html,
#     inputs=[],  # no inputs
#     outputs=gr.HTML(),  # render HTML directly
#     title="View All Transcriptions",
#     description="This table shows all saved transcriptions with User Name and Email."
# )

# iface.launch()

import gradio as gr
import sqlite3
import pandas as pd

DB_NAME = "transcribe.db"

def view_database_html():
    """Fetch all patient records (with Name + Email)."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name, email, audio_file, transcription, score, label, language, created_at
        FROM transcriptions
        ORDER BY created_at DESC
    """)
    rows = cursor.fetchall()
    conn.close()

    df = pd.DataFrame(
        rows,
        columns=["Name", "Email", "Audio File", "Transcription", "Score", "Label", "Language", "Created At"]
    )
    if df.empty:
        return "<p>No records found.</p>"

    return df.to_html(index=False, escape=False)

iface = gr.Interface(
    fn=view_database_html,
    inputs=[],
    outputs=gr.HTML(),
    title="Patient Records",
    description="All stored patient records with Name + Email."
)

iface.launch()
