import librosa
import re

def analyze_pitch(transcript, audio_path):
    # Load audio and compute duration
    y, sr = librosa.load(audio_path)
    duration_sec = librosa.get_duration(y=y, sr=sr)
    total_words = len(transcript.split()) if transcript else 0
    minutes = duration_sec / 60.0 if duration_sec > 0 else 1

    # ----- 1. Pacing (score: 0-10) -----
    wpm = total_words / minutes if minutes else 0
    if 120 <= wpm <= 150:
        pacing = 10
    elif 100 <= wpm < 120 or 150 < wpm <= 170:
        pacing = 8
    elif 80 <= wpm < 100 or 170 < wpm <= 190:
        pacing = 6
    else:
        pacing = 3  # Too slow or fast

    # ----- 2. Filler Words (density, per 100 words; score: 0-10) -----
    filler_phrases = ["um", "uh", "like", "you know", "so", "actually", "basically"]
    filler_matches = [len(re.findall(r"\b%s\b" % f, transcript.lower())) for f in filler_phrases]
    filler_total = sum(filler_matches)
    filler_rate_per_100 = (filler_total/total_words)*100 if total_words > 0 else 0

    if filler_rate_per_100 < 2:
        filler_score = 10
    elif filler_rate_per_100 < 4:
        filler_score = 8
    elif filler_rate_per_100 < 6:
        filler_score = 6
    elif filler_rate_per_100 < 10:
        filler_score = 4
    else:
        filler_score = 2

    # ----- 3. Fumbling (self-repair / repetition, score: 0-10) -----
    fumbling_phrases = ["i mean", "what i meant", "sorry", "let me rephrase", "well,"]
    fumbling_total = sum(len(re.findall(r"\b%s\b" % f, transcript.lower())) for f in fumbling_phrases)
    # Heavily penalized if fumbling occurs often
    if fumbling_total == 0:
        fumbling_score = 10
    elif fumbling_total <= 1:
        fumbling_score = 8
    elif fumbling_total <= 2:
        fumbling_score = 6
    elif fumbling_total <= 4:
        fumbling_score = 4
    else:
        fumbling_score = 2

    # ----- 4. Structure (detects pitch sections, score: 0-10) -----
    structure_sections = {
        "problem": ["problem", "challenge", "pain point"],
        "solution": ["solution", "we solve", "we provide", "address", "offering"],
        "market": ["market", "customers", "target audience", "user base"],
        "traction": ["traction", "growth", "revenue", "milestone", "users", "customers"],
        "ask": ["ask", "funding", "investment", "looking for", "partner", "support"]
    }
    found_sections = 0
    t_lower = transcript.lower()
    for sect, keywords in structure_sections.items():
        if any(k in t_lower for k in keywords):
            found_sections += 1
    structure_score = int((found_sections / len(structure_sections)) * 10)

    # ----- 5. Weighted Total Score -----
    # Emphasize structure and fluency, but pacing still matters
    total_score = round(
        0.30 * structure_score +
        0.25 * pacing +
        0.20 * filler_score +
        0.15 * fumbling_score +
        0.10 * min(10, total_words/50), # 10 points for >500 words else linear
        1
    )

    # ----- 6. Confidence -----
    if structure_score < 5 or pacing < 5 or filler_score < 5:
        confidence = "Low 😟"
    elif total_score > 8:
        confidence = "High 😎"
    else:
        confidence = "Moderate 🙂"

    metrics = {
        "pacing": pacing,
        "filler_words": filler_score,
        "fumbling": fumbling_score,
        "pitch_structure": structure_score,
        "total_score": total_score,
    }
    return duration_sec, metrics, confidence
