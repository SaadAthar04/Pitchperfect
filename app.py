import tempfile
import streamlit as st
import time
import os
from streamlit_mic_recorder import mic_recorder as st_mic_recorder
from speech_analysis import analyze_pace, analyze_tone, detect_filler_words
from utils import transcribe_audio, plot_wave_analysis, convert_to_wav

# Set page config
st.set_page_config(page_title="PitchPerfect - Presentation Trainer", page_icon="🎤")

st.title("🎤 PitchPerfect - AI-Powered Presentation Trainer")
st.subheader("Improve your speech clarity, tone, and pace!")

#st.header("📂 Upload Pre-Recorded Audio")

audio_file = None  # Initialize audio_file variable

option = st.selectbox("Choose input method", ["Record Audio", "Upload File"])

audio_file = None

if option == "Record Audio":
    recorded_audio = st_mic_recorder(start_prompt="🎤 Click to record", key="mic")
    if recorded_audio and isinstance(recorded_audio, dict) and 'bytes' in recorded_audio:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            temp_audio.write(recorded_audio['bytes'])
            temp_audio_path = temp_audio.name  # Use temp file path
        audio_file = temp_audio_path

elif option == "Upload File":
    uploaded_file = st.file_uploader("Upload an audio file", type=["wav", "mp3"])
    if uploaded_file:
        if uploaded_file.type == "audio/mpeg":  # Convert MP3 to WAV
            st.write("🔄 **Converting MP3 to WAV...**")
            audio_file = convert_to_wav(uploaded_file)
            if not audio_file:
                st.error("❌ Error: Could not convert MP3 to WAV.")
                st.stop()
        else:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
                temp_audio.write(uploaded_file.read())
                audio_file = temp_audio.name
        st.audio(audio_file, format="audio/wav")


# Process the audio file if available
if audio_file:
    st.audio(audio_file, format="audio/wav")

    with st.status("⏳ Processing your audio...", expanded=True) as status:
        # 1️⃣ Transcription
        with st.spinner("🔄 **Step 1:** Transcribing your speech..."):
            transcription = transcribe_audio(audio_file)
            time.sleep(2)
        st.success("✅ **Done!** Transcription complete.")

        # 2️⃣ Filler Words Analysis
        with st.spinner("🔄 **Step 2:** Detecting filler words..."):
            filler_analysis = detect_filler_words(transcription)
            time.sleep(1)
        st.success(f"✅ **Done!** Found: {filler_analysis}" if filler_analysis else "✅ No filler words detected!")

        # 3️⃣ Pace Analysis
        with st.spinner("🔄 **Step 3:** Analyzing speech pace..."):
            tempo = analyze_pace(audio_file)
            time.sleep(1)
        st.success(f"✅ **Done!** Speech tempo: **{tempo} BPM**")

        # 4️⃣ Tone Analysis
        with st.spinner("🔄 **Step 4:** Analyzing tone (pitch)..."):
            tone = analyze_tone(audio_file)
            time.sleep(1)
        st.success(f"✅ **Done!** Average pitch: **{tone} Hz**")

        status.update(label="🎉 All analysis completed!", state="complete")

    # 📊 Visualization
    st.header("📊 Tone & Pace Visualization")
    fig = plot_wave_analysis(tempo, tone)
    st.pyplot(fig)

    # 📌 Pace Feedback
    if tempo < 110:
        st.warning(f"🟡 Your speech is **too slow** at {tempo} BPM. Try speaking a bit faster for a more engaging delivery.")
    elif tempo > 160:
        st.warning(f"🟡 Your speech is **too fast** at {tempo} BPM. Consider slowing down to improve clarity.")
    else:
        st.success("✅ Your speech pace is **ideal!** Keep it up!")

    # 📌 Tone Feedback
    if tone < 85:
        st.warning(f"🟡 Your pitch is quite **low** at {round(tone, 2)} Hz. If your voice sounds too deep or unclear, try modulating it.")
    elif tone > 255:
        st.warning(f"🟡 Your pitch is quite **high** at {round(tone, 2)} Hz. If it sounds too sharp, consider lowering your tone slightly.")
    else:
        st.success("✅ Your pitch is within a **good range!** Well done.")

else:
    st.warning("⚠️ Please record or upload an audio file to proceed.")