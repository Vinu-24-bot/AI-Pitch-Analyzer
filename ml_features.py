# ml_features.py
import librosa
import re

def extract_features(transcript, audio_path):
    y, sr = librosa.load(audio_path)
    duration_sec = librosa.get_duration(y=y, sr=sr)
    total_words = len(transcript.split()) if transcript else 0
    minutes = duration_sec / 60.0 if duration_sec > 0 else 1
    wpm = total_words / minutes if minutes else 0

    filler_phrases = ["um", "uh", "like", "you know", "so", "actually", "basically"]
    filler_count = sum(len(re.findall(r"\b%s\b" % f, transcript.lower())) for f in filler_phrases)
    filler_rate = (filler_count / total_words) * 100 if total_words > 0 else 0

    fumbling_phrases = ["i mean", "what i meant", "sorry", "let me rephrase", "well,"]
    fumbling_count = sum(len(re.findall(r"\b%s\b" % f, transcript.lower())) for f in fumbling_phrases)

    structure_sections = {
        "problem": ["problem", "challenge", "pain point"],
        "solution": ["solution", "we solve", "we provide"],
        "market": ["market", "target audience"],
        "traction": ["traction", "growth", "revenue"],
        "ask": ["ask", "funding", "investment"]
    }
    t_lower = transcript.lower()
    structure_score = sum(any(k in t_lower for k in keywords) for keywords in structure_sections.values())

    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    rms_energy = float(librosa.feature.rms(y=y).mean())

    return [duration_sec, wpm, filler_rate, fumbling_count, structure_score, tempo, rms_energy]
