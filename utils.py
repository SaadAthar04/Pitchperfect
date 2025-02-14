import whisper
import matplotlib.pyplot as plt
import tempfile
import librosa
import soundfile as sf
import numpy as np

def convert_to_wav(uploaded_file):
    """ Convert an uploaded MP3 file to WAV format for processing. """
    try:
        # Create a temporary WAV file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_wav:
            y, sr = librosa.load(uploaded_file, sr=None)  # Load audio
            sf.write(temp_wav.name, y, sr)  # Save as WAV
            return temp_wav.name  # Return path of the WAV file
    except Exception as e:
        return None


def transcribe_audio(audio_input):
    model = whisper.load_model("base")

    # Handle UploadedFile object from Streamlit
    if hasattr(audio_input, "read"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            temp_audio.write(audio_input.read())
            temp_audio_path = temp_audio.name
        audio_input = temp_audio_path  # Use the temp file path instead

    result = model.transcribe(audio_input)
    return result["text"]


def plot_wave_analysis(tempo, tone, avg_tempo=135, avg_tone=170):
    x = np.linspace(0, 2 * np.pi, 400)
    user_tempo_wave = np.sin(x * tempo / 20)
    avg_tempo_wave = np.sin(x * avg_tempo / 20)
    
    user_tone_wave = np.sin(x * tone / 50)
    avg_tone_wave = np.sin(x * avg_tone / 50)
    
    fig, ax = plt.subplots(2, 1, figsize=(6, 6))
    
    # Pace Wave
    ax[0].plot(x, user_tempo_wave, label=f"Your Pace ({tempo} BPM)", color='blue')
    ax[0].plot(x, avg_tempo_wave, linestyle='dashed', label=f"Average Pace ({avg_tempo} BPM)", color='red')
    ax[0].set_title("Speech Pace Analysis")
    ax[0].legend()
    ax[0].set_xticks([])
    ax[0].set_yticks([])
    
    # Tone Wave
    ax[1].plot(x, user_tone_wave, label=f"Your Tone ({round(tone, 2)} Hz)", color='green')
    ax[1].plot(x, avg_tone_wave, linestyle='dashed', label=f"Average Tone ({avg_tone} Hz)", color='orange')
    ax[1].set_title("Speech Tone Analysis")
    ax[1].legend()
    ax[1].set_xticks([])
    ax[1].set_yticks([])
    
    plt.tight_layout()
    return fig