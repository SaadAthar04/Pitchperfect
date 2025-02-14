import librosa
import numpy as np
import re

def analyze_pace(audio_file):
    y, sr = librosa.load(audio_file, sr=None)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    
    if isinstance(tempo, (list, np.ndarray)):  # Ensure it's a scalar value
        tempo = float(tempo[0]) if len(tempo) > 0 else 0.0

    return round(tempo, 2)


def analyze_tone(audio_file):
    y, sr = librosa.load(audio_file, sr=None)
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
    avg_pitch = np.nanmean(pitches[pitches > 0])
    return round(avg_pitch, 2) if not np.isnan(avg_pitch) else 0

def detect_filler_words(text):
    fillers = ["um", "uh", "like", "you know", "so", "actually"]
    filler_count = {word: len(re.findall(rf"\b{word}\b", text, re.IGNORECASE)) for word in fillers}
    return {word: count for word, count in filler_count.items() if count > 0}