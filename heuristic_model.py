# # heuristic_model.py
# from pydub import AudioSegment, silence

# FILLERS = ["um", "uh", "hmm", "erm", "ah", "like", "you know"]

# def extract_features(audio_path, transcript):
#     audio = AudioSegment.from_file(audio_path)
#     duration = len(audio) / 1000.0  # seconds
#     words = len(transcript.split())
#     speech_rate = words / duration if duration > 0 else 0

#     # Pauses longer than 400ms
#     sil = silence.detect_silence(audio, min_silence_len=400, silence_thresh=-40)
#     total_pause = sum((e - s)/1000.0 for s, e in sil)
#     pause_ratio = total_pause / duration if duration > 0 else 0

#     filler_count = sum(transcript.lower().count(f) for f in FILLERS)

#     return {
#         "duration": duration,
#         "words": words,
#         "speech_rate": speech_rate,
#         "pause_ratio": pause_ratio,
#         "filler_count": filler_count
#     }

# def risk_score(features):
#     sr = features["speech_rate"]
#     pr = features["pause_ratio"]
#     fc = features["filler_count"]

#     score = 0
#     if sr < 1.8:  # low speech rate
#         score += (1.8 - sr)/1.8 * 50
#     score += min(pr, 0.8)/0.8 * 40
#     score += min(fc, 10)/10 * 10
#     score = max(0, min(100, score))

#     if score >= 60:
#         label = "High risk — recommend clinical referral"
#     elif score >= 30:
#         label = "Medium risk — monitor / repeat test"
#     else:
#         label = "Low risk"

#     explanation = f"speech_rate={sr:.2f} wps, pause_ratio={pr:.2f}, fillers={fc}"
#     return score, label, explanation


# heuristic_model.py
from pydub import AudioSegment, silence

FILLERS = ["um", "uh", "hmm", "erm", "ah", "like", "you know"]

def extract_features(audio_path, transcript):
    """
    Extract speech features from audio and transcript.
    Returns a dict with duration, words, speech_rate, pause_ratio, filler_count.
    """
    audio = AudioSegment.from_file(audio_path)
    duration = len(audio) / 1000.0  # seconds
    words = len(transcript.split())
    speech_rate = words / duration if duration > 0 else 0

    # Detect pauses longer than 400ms
    sil = silence.detect_silence(audio, min_silence_len=400, silence_thresh=-40)
    total_pause = sum((e - s)/1000.0 for s, e in sil)
    pause_ratio = total_pause / duration if duration > 0 else 0

    filler_count = sum(transcript.lower().count(f) for f in FILLERS)

    return {
        "duration": duration,
        "words": words,
        "speech_rate": speech_rate,
        "pause_ratio": pause_ratio,
        "filler_count": filler_count
    }

def risk_score(features):
    """
    Compute dementia risk score (0-100) and label based on speech features.
    Returns: score, label, explanation
    """
    sr = features["speech_rate"]
    pr = features["pause_ratio"]
    fc = features["filler_count"]

    score = 0
    if sr < 1.8:  # low speech rate
        score += (1.8 - sr)/1.8 * 50
    score += min(pr, 0.8)/0.8 * 40
    score += min(fc, 10)/10 * 10
    score = max(0, min(100, score))

    if score >= 60:
        label = "High risk — recommend clinical referral"
    elif score >= 30:
        label = "Medium risk — monitor / repeat test"
    else:
        label = "Low risk"

    explanation = f"speech_rate={sr:.2f} wps, pause_ratio={pr:.2f}, fillers={fc}"
    return score, label, explanation

def analyze_dementia(audio_path, transcript):
    """
    Main function to get dementia score from audio & transcription.
    Returns normalized 0-1 score for DB storage.
    """
    features = extract_features(audio_path, transcript)
    score, label, explanation = risk_score(features)
    normalized_score = round(score / 100, 2)  # store 0-1 in DB
    return normalized_score
