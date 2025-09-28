# transcribe.py
import whisper

# Load the Whisper model (you can choose "base", "small", "medium", "large")
model = whisper.load_model("base")

def transcribe_audio(audio_file_path, language=None):
    """
    Transcribe an audio file to text.
    
    Parameters:
    - audio_file_path: str, path to the audio file
    - language: str, optional, language code like 'en' or 'kn' for Kannada
    
    Returns:
    - str: transcribed text
    """
    try:
        result = model.transcribe(audio_file_path, language=language)
        return result["text"]
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        return None

# Optional: test transcription if run directly
if __name__ == "__main__":
    audio_path = "example_audio.wav"  # replace with your audio file
    lang = "en"  # or "kn" for Kannada
    text = transcribe_audio(audio_path, lang)
    print("Transcription result:")
    print(text)
