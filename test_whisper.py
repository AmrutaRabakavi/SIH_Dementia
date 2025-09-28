import whisper

model = whisper.load_model("small")  # small model is fast for demo
result = model.transcribe("Test.mp3.mp3")  # replace with your audio file path
print("Transcript:")
print(result["text"])
