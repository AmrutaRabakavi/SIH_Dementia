# import gradio as gr
# import sqlite3
# import pandas as pd

# DB_NAME = "transcribe.db"
# STAFF_PASSWORD = "admin123"  # Change this to your desired password

# def generate_full_csv(password):
#     """Verify password, then generate CSV of all transcriptions."""
#     if password != STAFF_PASSWORD:
#         return "Incorrect password. Access denied.", None

#     conn = sqlite3.connect(DB_NAME)
#     cursor = conn.cursor()
#     cursor.execute(
#         "SELECT user_id, audio_file, transcription, language, created_at FROM transcriptions"
#     )
#     rows = cursor.fetchall()
#     conn.close()

#     if not rows:
#         return "No transcriptions available.", None

#     df = pd.DataFrame(rows, columns=["User ID", "Audio File", "Transcription", "Language", "Created At"])
#     csv_file = "all_transcriptions.csv"
#     df.to_csv(csv_file, index=False, encoding='utf-8')

#     return "Access granted! Download the CSV below.", csv_file

# # ---------------- Gradio Interface ---------------- #
# with gr.Blocks(title="Staff Access - Download Transcriptions") as demo:
#     gr.Markdown("## Staff Access: Enter Password to Download All Transcriptions")
    
#     password_input = gr.Textbox(label="Enter Staff Password", type="password")  # <-- FIXED
#     status_text = gr.Textbox(label="Status", interactive=False)
#     download_csv = gr.File(label="Download Full Transcriptions CSV")
#     submit_btn = gr.Button("Submit")
    
#     submit_btn.click(
#         fn=generate_full_csv,
#         inputs=[password_input],
#         outputs=[status_text, download_csv]
#     )

# demo.launch()



# staff_access.py
# import gradio as gr
# import sqlite3
# import pandas as pd

# DB_NAME = "transcribe.db"
# STAFF_PASSWORD = "admin123"  # Change as needed

# def generate_full_csv(password):
#     """Verify password and generate CSV of all transcriptions + dementia score."""
#     if password != STAFF_PASSWORD:
#         return "Incorrect password. Access denied.", None

#     conn = sqlite3.connect(DB_NAME)
#     cursor = conn.cursor()
#     cursor.execute("""
#         SELECT user_id, audio_file, transcription, language, created_at, dementia_score
#         FROM transcriptions
#     """)
#     rows = cursor.fetchall()
#     conn.close()

#     if not rows:
#         return "No transcriptions available.", None

#     df = pd.DataFrame(rows, columns=[
#         "User ID", "Audio File", "Transcription", "Language", "Created At", "Dementia Score"
#     ])
#     csv_file = "all_transcriptions_dementia.csv"
#     df.to_csv(csv_file, index=False, encoding='utf-8')

#     return "Access granted! Download the CSV below.", csv_file

# with gr.Blocks(title="Staff Access - Dementia Transcriptions") as demo:
#     gr.Markdown("## Staff Access: Enter Password to Download All Transcriptions & Dementia Scores")
    
#     password_input = gr.Textbox(label="Enter Staff Password", type="password")
#     status_text = gr.Textbox(label="Status", interactive=False)
#     download_csv = gr.File(label="Download Full Transcriptions CSV")
    
#     submit_btn = gr.Button("Submit")
#     submit_btn.click(
#         fn=generate_full_csv,
#         inputs=[password_input],
#         outputs=[status_text, download_csv]
#     )

# demo.launch()




# # staff_access.py
# import gradio as gr
# import sqlite3
# import pandas as pd

# # Staff password (change this securely later)
# STAFF_PASSWORD = "admin123"

# def check_access(password):
#     if password != STAFF_PASSWORD:
#         return "❌ Invalid password.", None, None
    
#     # Connect DB
#     conn = sqlite3.connect("results.db")
#     df = pd.read_sql_query("SELECT * FROM transcriptions", conn)
#     conn.close()

#     # Show table + CSV
#     return "✅ Access granted.", df, df.to_csv(index=False)


# with gr.Blocks() as demo:
#     gr.Markdown("## 👩‍⚕️ Staff Access Dashboard")
#     gr.Markdown("Enter staff password to view results.")

#     password = gr.Textbox(label="Password", type="password")
#     submit = gr.Button("Login")

#     status = gr.Textbox(label="Status")
#     table = gr.DataFrame(label="Transcriptions Table", visible=True)
#     download = gr.File(label="Download CSV", visible=True)

#     submit.click(fn=check_access,
#                  inputs=password,
#                  outputs=[status, table, download])

# demo.launch()




import gradio as gr
import sqlite3
import pandas as pd

DB_NAME = "transcribe.db"
STAFF_PASSWORD = "admin123"  # Change this securely

def check_access(password):
    if password != STAFF_PASSWORD:
        return "❌ Invalid password.", None, None
    
    # Connect DB and fetch all transcriptions
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM transcriptions", conn)
    conn.close()

    # Save CSV to file
    csv_file = "all_transcriptions.csv"
    df.to_csv(csv_file, index=False, encoding="utf-8")

    return "✅ Access granted.", df, csv_file  # DataFrame for table, file path for download

with gr.Blocks() as demo:
    gr.Markdown("## 👩‍⚕️ Staff Access Dashboard")
    gr.Markdown("Enter staff password to view results and download CSV.")

    password_input = gr.Textbox(label="Password", type="password")
    submit_btn = gr.Button("Login")

    status_output = gr.Textbox(label="Status", interactive=False)
    table_output = gr.DataFrame(label="Transcriptions Table")
    download_output = gr.File(label="Download CSV")

    submit_btn.click(
        fn=check_access,
        inputs=password_input,
        outputs=[status_output, table_output, download_output]
    )

demo.launch()
