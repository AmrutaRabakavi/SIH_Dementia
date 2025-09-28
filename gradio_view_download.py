# # gradio_view_download.py
# import gradio as gr
# import sqlite3
# import pandas as pd

# DB_NAME = "transcribe.db"

# def get_transcriptions():
#     """Fetch all transcriptions and return both HTML table and CSV file path."""
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

#     if not rows:
#         html_table = "<p>No transcriptions found.</p>"
#         return html_table, None

#     # Build HTML table manually
#     html = "<table border='1' style='border-collapse: collapse; width: 100%;'>"
#     html += "<tr><th>ID</th><th>User Name</th><th>Email</th><th>Audio File</th><th>Transcription</th><th>Language</th><th>Created At</th></tr>"
#     for row in rows:
#         html += "<tr>" + "".join([f"<td>{col}</td>" for col in row]) + "</tr>"
#     html += "</table>"

#     # Save CSV for download
#     df = pd.DataFrame(rows, columns=["ID", "User Name", "Email", "Audio File", "Transcription", "Language", "Created At"])
#     csv_file = "transcriptions.csv"
#     df.to_csv(csv_file, index=False, encoding='utf-8')

#     return html, csv_file

# iface = gr.Interface(
#     fn=get_transcriptions,
#     inputs=[],
#     outputs=[gr.HTML(), gr.File(label="Download Table as CSV")],
#     title="View & Download Transcriptions",
#     description="Click 'Submit' to generate a clean table of all saved transcriptions and download it as a CSV file."
# )

# iface.launch()




import gradio as gr
import sqlite3
import pandas as pd

DB_NAME = "transcribe.db"
STAFF_PASSWORD = "admin123"  # Same as in main app

# ---------------- Staff Access Function ---------------- #
def generate_csv(password):
    if password != STAFF_PASSWORD:
        return "❌ Invalid password", None, None

    # Connect to DB
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM transcriptions", conn)
    conn.close()

    if df.empty:
        return "⚠️ No transcriptions available", None, None

    # Save CSV
    csv_file = "all_transcriptions.csv"
    df.to_csv(csv_file, index=False, encoding="utf-8")

    return "✅ Access granted", df, csv_file

# ---------------- Gradio UI ---------------- #
with gr.Blocks() as demo:
    gr.Markdown("## 👩‍⚕️ Staff Access Dashboard")
    gr.Markdown("Enter password to view all transcriptions and download CSV.")

    password_input = gr.Textbox(label="Password", type="password")
    submit_btn = gr.Button("Login")

    status_out = gr.Textbox(label="Status", interactive=False)
    table_out = gr.DataFrame(label="Transcriptions Table")
    download_csv = gr.File(label="Download CSV")

    submit_btn.click(
        fn=generate_csv,
        inputs=password_input,
        outputs=[status_out, table_out, download_csv]
    )

demo.launch()

