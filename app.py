import os
import uuid
import threading
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from yt_dlp import YoutubeDL

from utils.audio_tools import extract_audio
from utils.transcription import transcribe_audio
from utils.speech_analysis import analyze_pitch

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def download_youtube(youtube_link, video_path):
    ydl_opts = {
        'format': 'mp4',
        'outtmpl': video_path,
        'retries': 2,
        'quiet': True
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_link])

def cleanup_files(*paths):
    import time
    time.sleep(45)
    for p in paths:
        try:
            os.remove(p)
        except Exception:
            pass

@app.route('/', methods=['GET', 'POST'])
def upload_pitch():
    if request.method == 'POST':
        startup = request.form.get('startup')
        pitch_date = request.form.get('pitch_date')
        youtube_link = request.form.get('youtube_link', '').strip()
        video_file = request.files.get('pitch')
        error = None

        video_path = None
        filename = None
        unique_id = str(uuid.uuid4())

        if youtube_link:
            try:
                filename = f"youtube_pitch_{unique_id}.mp4"
                video_path = os.path.join(UPLOAD_FOLDER, filename)
                download_youtube(youtube_link, video_path)
            except Exception as e:
                print("[yt-dlp ERROR]:", e)
                return render_template('index.html', error="Failed to download YouTube video. Please check the link.")
        elif video_file and video_file.filename:
            ext = os.path.splitext(video_file.filename)[-1]
            base = os.path.splitext(secure_filename(video_file.filename))[0]
            filename = f"{base}_{unique_id}{ext}"
            video_path = os.path.join(UPLOAD_FOLDER, filename)
            video_file.save(video_path)
        else:
            return render_template('index.html', error="Please upload a video file or provide a YouTube link.")

        base, _ = os.path.splitext(video_path)
        audio_path = f"{base}.wav"
        try:
            extract_audio(video_path, audio_path)
        except Exception as e:
            print("Audio extraction error:", e)
            return render_template('index.html', error="Failed to extract audio from video file.")

        transcript = transcribe_audio(audio_path)
        duration, metrics, confidence = analyze_pitch(transcript, audio_path)
        file_format = filename.split('.')[-1]

        threading.Thread(target=cleanup_files, args=(video_path, audio_path)).start()

        return render_template(
            'result.html',
            startup=startup,
            pitch_date=pitch_date,
            duration=f"{duration:.2f} seconds",
            transcript=transcript,
            file_format=file_format.upper(),
            metrics=metrics,
            confidence=confidence
        )
    return render_template('index.html')

# ✅ Use waitress for stable deployment
if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)
