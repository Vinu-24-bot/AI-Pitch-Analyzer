import os
import pandas as pd
import joblib
import numpy as np
from ml_features import extract_features
from transcription import transcribe_audio
from audio_tools import extract_audio
from sklearn.multioutput import MultiOutputRegressor
from sklearn.ensemble import RandomForestRegressor

VIDEO_DIR = "training_videos"
AUDIO_DIR = "training_audio"
LABEL_FILE = "multi_labels.csv"
MODEL_PATH = "pitch_model.pkl"

def clean_features(features):
    """Ensure all values are float and fix nested arrays"""
    cleaned = []
    for f in features:
        if isinstance(f, np.ndarray):
            # e.g. array([123.0]) → 123.0
            cleaned.append(float(f.item()))
        elif isinstance(f, (int, float, np.integer, np.floating)):
            cleaned.append(float(f))
        else:
            # fallback for weird data
            try:
                cleaned.append(float(f))
            except:
                cleaned.append(0.0)
    return cleaned if len(cleaned) == 7 else None

def train():
    df = pd.read_csv(LABEL_FILE)
    X, Y = [], []

    for index, row in df.iterrows():
        video_file = row['filename']
        video_path = os.path.join(VIDEO_DIR, video_file)
        audio_path = os.path.join(AUDIO_DIR, video_file.replace('.mp4', '.wav'))

        try:
            extract_audio(video_path, audio_path)
            transcript = transcribe_audio(audio_path)
            raw_features = extract_features(transcript, audio_path)
            features = clean_features(raw_features)

            if not features:
                print(f"⚠️ Could not clean features for {video_file}. Using zeros.")
                features = [0.0] * 7

            label_vector = [
                row['pacing'], row['filler_words'],
                row['fumbling'], row['pitch_structure'],
                row['total_score']
            ]

            X.append(features)
            Y.append(label_vector)

        except Exception as e:
            print(f"❌ ERROR in {video_file}: {e}")

    if not X:
        print("❌ No valid training data found. Aborting.")
        return

    print(f"✅ Training on {len(X)} samples...")
    model = MultiOutputRegressor(RandomForestRegressor(n_estimators=150, random_state=42))
    model.fit(X, Y)
    joblib.dump(model, MODEL_PATH)
    print(f"🎯 Model trained and saved at: {MODEL_PATH}")

if __name__ == "__main__":
    train()
import os
import pandas as pd
import joblib
import numpy as np
from ml_features import extract_features
from transcription import transcribe_audio
from audio_tools import extract_audio
from sklearn.multioutput import MultiOutputRegressor
from sklearn.ensemble import RandomForestRegressor

VIDEO_DIR = "training_videos"
AUDIO_DIR = "training_audio"
LABEL_FILE = "multi_labels.csv"
MODEL_PATH = "pitch_model.pkl"

def clean_features(features):
    """Ensure all values are float and fix nested arrays"""
    cleaned = []
    for f in features:
        if isinstance(f, np.ndarray):
            # e.g. array([123.0]) → 123.0
            cleaned.append(float(f.item()))
        elif isinstance(f, (int, float, np.integer, np.floating)):
            cleaned.append(float(f))
        else:
            # fallback for weird data
            try:
                cleaned.append(float(f))
            except:
                cleaned.append(0.0)
    return cleaned if len(cleaned) == 7 else None

def train():
    df = pd.read_csv(LABEL_FILE)
    X, Y = [], []

    for index, row in df.iterrows():
        video_file = row['filename']
        video_path = os.path.join(VIDEO_DIR, video_file)
        audio_path = os.path.join(AUDIO_DIR, video_file.replace('.mp4', '.wav'))

        try:
            extract_audio(video_path, audio_path)
            transcript = transcribe_audio(audio_path)
            raw_features = extract_features(transcript, audio_path)
            features = clean_features(raw_features)

            if not features:
                print(f"⚠️ Could not clean features for {video_file}. Using zeros.")
                features = [0.0] * 7

            label_vector = [
                row['pacing'], row['filler_words'],
                row['fumbling'], row['pitch_structure'],
                row['total_score']
            ]

            X.append(features)
            Y.append(label_vector)

        except Exception as e:
            print(f"❌ ERROR in {video_file}: {e}")

    if not X:
        print("❌ No valid training data found. Aborting.")
        return

    print(f"✅ Training on {len(X)} samples...")
    model = MultiOutputRegressor(RandomForestRegressor(n_estimators=150, random_state=42))
    model.fit(X, Y)
    joblib.dump(model, MODEL_PATH)
    print(f"🎯 Model trained and saved at: {MODEL_PATH}")

if __name__ == "__main__":
    train()
