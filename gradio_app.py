# gradio_app.py
import gradio as gr
import re
import whisper
from heuristic_model import extract_features, risk_score
from app import insert_transcription
import subprocess
import webbrowser
import time
import threading

# Whisper model
whisper_model = whisper.load_model("base")

# ---------------- Validation ---------------- #
def is_valid_name(name):
    return bool(re.fullmatch(r"[A-Za-z ]+", name.strip()))

def is_valid_email(email):
    return bool(re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email.strip()))

# ---------------- User Processing ---------------- #
def process_audio(name, email, audio_file):
    name_valid = is_valid_name(name)
    email_valid = is_valid_email(email)

    if not name_valid and not email_valid:
        return "", "", "❌ Invalid Name and Email"
    elif not name_valid:
        return "", "", "❌ Invalid Name (letters and spaces only)"
    elif not email_valid:
        return "", "", "❌ Invalid Email format"

    if audio_file is None:
        return "", "", "❌ Please upload or record an audio file."

    try:
        result = whisper_model.transcribe(audio_file)
        transcript = result["text"]

        features = extract_features(audio_file, transcript)
        score, label, explanation = risk_score(features)

        # ✅ Save name + email directly in DB
        insert_transcription(name, email, audio_file, transcript, score, label)

        return f"Risk: {label} (Score={score:.1f})", explanation, "✅ Success"
    except Exception as e:
        return "", "", f"❌ Error processing audio: {str(e)}"

# ---------------- Staff Page Redirect ---------------- #
def open_staff_page():
    def launch_staff():
        subprocess.Popen(["python", "gradio_view_db_html.py"])
    threading.Thread(target=launch_staff).start()
    time.sleep(2)
    webbrowser.open("http://127.0.0.1:7861")
    return "✅ Staff page launched in a new browser tab"

# ---------------- Gradio UI ---------------- #
with gr.Blocks() as demo:
    gr.Markdown("## 🧠 Dementia Screening Tool")

    # User inputs
    name_input = gr.Textbox(label="Name *")
    email_input = gr.Textbox(label="Email *")
    audio_input = gr.Audio(sources=["microphone", "upload"], type="filepath", label="Upload Audio")
    submit_btn = gr.Button("Analyze Speech")

    risk_out = gr.Textbox(label="Risk Score")
    explanation_out = gr.Textbox(label="Feature Explanation")
    status_out = gr.Textbox(label="Status / Validation", interactive=False)

    submit_btn.click(
        fn=process_audio,
        inputs=[name_input, email_input, audio_input],
        outputs=[risk_out, explanation_out, status_out]
    )

    gr.Markdown("---")
    gr.Markdown("### Staff Only")
    staff_btn = gr.Button("Staff Access (Password Required)")
    staff_btn.click(fn=open_staff_page, inputs=[], outputs=status_out)

demo.launch()
