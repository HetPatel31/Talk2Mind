import streamlit as st
import cv2
import numpy as np
from PIL import Image
from modules.face.visual_pipeline import VisualEmotionClassifier

st.set_page_config(page_title="Face Analysis", page_icon="😊", layout="wide")

st.title("😊 Face Emotion Analysis")
st.caption("Analyze facial expressions using the Talk2Mind computer vision pipeline.")

@st.cache_resource
def load_classifier():
    return VisualEmotionClassifier()

classifier = load_classifier()

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📷 Camera Input")
    captured_image = st.camera_input(
        "Capture an image for emotion analysis"
    )

with col2:
    st.subheader("🎯 Analysis Output")

    if captured_image is None:
        st.metric("Detected Emotion", "Waiting...")
        st.metric("Confidence", "0%")

if captured_image is not None:
    image = Image.open(captured_image)
    image_np = np.array(image)

    frame = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

    result = classifier.predict_image(frame)

    st.session_state["face_emotion"] = result["emotion"]
    st.session_state["face_confidence"] = result["confidence"]

    st.image(
        cv2.cvtColor(result["frame"], cv2.COLOR_BGR2RGB),
        caption="Emotion Analysis Result",
        use_container_width=True
    )

    col_a, col_b = st.columns(2)

    with col_a:
        st.metric("Detected Emotion", result["emotion"])

    with col_b:
        st.metric("Confidence", f"{result['confidence']}%")

st.divider()

st.subheader("🧠 Supported Emotions")

c1, c2, c3, c4 = st.columns(4)
c1.success("😀 Happy")
c2.info("😐 Neutral")
c3.warning("😲 Surprise")
c4.error("😠 Angry")

c1, c2, c3 = st.columns(3)
c1.info("😢 Sad")
c2.info("😨 Fear")
c3.info("🤢 Disgust")