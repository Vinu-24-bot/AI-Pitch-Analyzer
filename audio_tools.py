from pydub import AudioSegment

def extract_audio(video_path, audio_path):
    audio = AudioSegment.from_file(video_path)
    audio.export(audio_path, format="wav")
