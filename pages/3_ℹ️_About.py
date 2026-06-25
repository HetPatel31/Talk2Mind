

import streamlit as st

st.set_page_config(page_title="About", page_icon="ℹ️", layout="wide")

st.title("ℹ️ About Talk2Mind")
st.caption("AI-Powered Multimodal Mental Well-Being Assessment Platform")

st.markdown("""
## 🧠 Project Overview

Talk2Mind is an AI-powered mental well-being assessment system that combines:

- 📝 Questionnaire-based assessment (PHQ-9 & GAD-7)
- 😊 Facial emotion recognition
- 🎤 Voice emotion analysis
- 🧠 Multimodal fusion for wellness insights

The goal is to provide users with a holistic view of their emotional and mental well-being.
""")

st.divider()

st.header("✨ Features")

col1, col2 = st.columns(2)

with col1:
    st.success("📝 PHQ-9 Depression Assessment")
    st.success("📝 GAD-7 Anxiety Assessment")
    st.success("😊 Facial Emotion Recognition")

with col2:
    st.success("🎤 Voice Emotion Analysis")
    st.success("🧠 Wellness Score Generation")
    st.success("📊 Interactive Results Dashboard")

st.divider()

st.header("⚙️ Technology Stack")

tech1, tech2, tech3, tech4, tech5 = st.columns(5)

tech1.info("Python")
tech2.info("PyTorch")
tech3.info("MediaPipe")
tech4.info("Librosa")
tech5.info("Streamlit")

st.divider()

st.header("🚀 Future Roadmap")

st.markdown("""
- Face Analysis Integration
- Voice Analysis Integration
- Multimodal Fusion Dashboard
- PDF Report Generation
- Cloud Deployment
- Historical Assessment Tracking
""")

st.divider()

st.header("👨‍💻 Developer")

st.markdown("""
**Het Patel**

Computer Science Engineering Student

Project: Talk2Mind – AI-Powered Mental Well-Being Assessment System
""")

st.divider()

st.caption("Talk2Mind v1.0 | Built with Streamlit, PyTorch, MediaPipe and Librosa")