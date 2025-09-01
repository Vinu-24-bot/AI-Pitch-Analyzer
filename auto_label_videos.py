import os
import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from transcription import transcribe_audio
from audio_tools import extract_audio
from speech_analysis import analyze_pitch

from tqdm import tqdm

VIDEO_DIR = "training_videos"
AUDIO_DIR = "training_audio"
OUT_CSV = "multi_labels.csv"

os.makedirs(AUDIO_DIR, exist_ok=True)

def process_videos():
    results = []

    for filename in tqdm(os.listdir(VIDEO_DIR)):
        if not filename.endswith(".mp4"):
            continue
        video_path = os.path.join(VIDEO_DIR, filename)
        audio_path = os.path.join(AUDIO_DIR, filename.replace(".mp4", ".wav"))

        try:
            extract_audio(video_path, audio_path)
            transcript = transcribe_audio(audio_path)
            _, metrics, _ = analyze_pitch(transcript, audio_path)

            results.append({
                "filename": filename,
                "pacing": metrics["pacing"],
                "filler_words": metrics["filler_words"],
                "fumbling": metrics["fumbling"],
                "pitch_structure": metrics["pitch_structure"],
                "total_score": metrics["total_score"]
            })
        except Exception as e:
            print(f"[ERROR]: {filename} → {e}")

    df = pd.DataFrame(results)
    df.to_csv(OUT_CSV, index=False)
    print(f"✅ Auto labels saved to {OUT_CSV}")

if __name__ == "__main__":
    process_videos()
