import os
from pydub import AudioSegment
import speech_recognition as sr

def transcribe_audio(audio_path, chunk_duration=45):
    recognizer = sr.Recognizer()
    audio = AudioSegment.from_file(audio_path)
    length_ms = len(audio)
    transcript = ""
    for i, start in enumerate(range(0, length_ms, chunk_duration * 1000)):
        end = min(start + chunk_duration * 1000, length_ms)
        chunk_audio = audio[start:end]
        chunk_path = f"{audio_path}_chunk_{i}.wav"
        chunk_audio.export(chunk_path, format="wav")
        with sr.AudioFile(chunk_path) as source:
            audio_data = recognizer.record(source)
            try:
                part = recognizer.recognize_google(audio_data)
            except sr.UnknownValueError:
                part = ""
            except sr.RequestError:
                part = "[Speech recognition failed for this segment.]"
        os.remove(chunk_path)
        transcript += " " + part
    return transcript.strip()
