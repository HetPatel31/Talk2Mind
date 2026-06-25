import streamlit as st
import tempfile
from modules.audio.speech_predictor import SpeechPredictor

st.set_page_config(page_title="Voice Analysis", page_icon="🎤", layout="wide")

st.title("🎤 Voice Emotion Analysis")
st.caption("Analyze emotional cues from speech and voice patterns.")

@st.cache_resource
def load_predictor():
    return SpeechPredictor()

predictor = load_predictor()

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🎙️ Voice Recording")
    audio_file = st.audio_input("Record your voice")

with col2:
    st.subheader("🎯 Analysis Output")

    if audio_file is None:
        st.metric("Detected Emotion", "Waiting...")
        st.metric("Confidence", "0%")

if audio_file is not None:

    st.audio(audio_file)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(audio_file.getvalue())
        temp_path = tmp.name

    result = predictor.predict_audio(temp_path)

    st.session_state["voice_emotion"] = result["emotion"]
    st.session_state["voice_confidence"] = result["confidence"]

    c1, c2 = st.columns(2)

    with c1:
        st.metric("Detected Emotion", result["emotion"])

    with c2:
        st.metric("Confidence", f"{result['confidence']}%")

    st.success(f"Predicted Emotion: {result['emotion']}")

st.divider()

st.subheader("🧠 Supported Emotions")

r1c1, r1c2, r1c3, r1c4 = st.columns(4)
r1c1.success("😀 Happy")
r1c2.info("😐 Neutral")
r1c3.warning("😲 Surprise")
r1c4.error("😠 Angry")

r2c1, r2c2, r2c3 = st.columns(3)
r2c1.info("😢 Sad")
r2c2.info("😨 Fear")
r2c3.info("🤢 Disgust")