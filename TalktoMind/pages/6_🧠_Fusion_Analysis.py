import streamlit as st
from utils.pdf_generator import generate_report
from pathlib import Path

st.set_page_config(page_title="Fusion Analysis", page_icon="🧠", layout="wide")

st.title("🧠 Multimodal Fusion Analysis")
st.caption("Automatically combines questionnaire, face emotion and voice emotion results.")

wellness_score = st.session_state.get("wellness_score", 0)
risk_level = st.session_state.get("risk_level", "Unknown")

face_emotion = st.session_state.get("face_emotion", "Not Available")
face_confidence = st.session_state.get("face_confidence", 0)

voice_emotion = st.session_state.get("voice_emotion", "Not Available")
voice_confidence = st.session_state.get("voice_confidence", 0)

depression_level = st.session_state.get("depression_level", "Unknown")
anxiety_level = st.session_state.get("anxiety_level", "Unknown")

st.subheader("📥 Collected Results")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Questionnaire Score", wellness_score)
    st.caption(f"Risk Level: {risk_level}")

with c2:
    st.metric("Face Emotion", face_emotion)
    st.caption(f"Confidence: {face_confidence:.2f}%")

with c3:
    st.metric("Voice Emotion", voice_emotion)
    st.caption(f"Confidence: {voice_confidence:.2f}%")

st.divider()

if st.button("🧠 Generate Final Fusion Assessment", use_container_width=True):

    fusion_score = (
        wellness_score * 0.6
        + face_confidence * 0.2
        + voice_confidence * 0.2
    )

    st.subheader("📊 Fusion Results")

    r1, r2, r3 = st.columns(3)

    with r1:
        st.metric("Final Wellness Score", f"{fusion_score:.1f}")

    with r2:
        st.metric("Depression Level", depression_level)

    with r3:
        st.metric("Anxiety Level", anxiety_level)

    if fusion_score >= 80:
        st.success("✅ Healthy Emotional State")

    elif fusion_score >= 60:
        st.warning("⚠️ Moderate Monitoring Recommended")

    else:
        st.error("🚨 High Attention Recommended")

    st.subheader("💡 Personalized Recommendations")

    recommendations = []

    if depression_level in ["Moderate", "Moderately Severe", "Severe"]:
        recommendations.append("Consider speaking with a mental health professional.")

    if anxiety_level in ["Moderate", "Severe"]:
        recommendations.append("Practice breathing exercises and stress management techniques.")

    recommendations.extend([
        "Maintain healthy sleep habits.",
        "Exercise regularly.",
        "Stay socially connected.",
        "Monitor emotional changes over time."
    ])

    for rec in recommendations:
        st.write(f"• {rec}")

    report_data = {
        "wellness_score": wellness_score,
        "risk_level": risk_level,
        "depression_level": depression_level,
        "anxiety_level": anxiety_level,
        "face_emotion": face_emotion,
        "face_confidence": face_confidence,
        "voice_emotion": voice_emotion,
        "voice_confidence": voice_confidence,
        "recommendations": recommendations
    }

    report_path = Path("reports") / "wellness_report.pdf"

    generate_report(
        str(report_path),
        report_data
    )

    with open(report_path, "rb") as pdf_file:
        st.download_button(
            label="📄 Download Wellness Report",
            data=pdf_file,
            file_name="Talk2Mind_Wellness_Report.pdf",
            mime="application/pdf",
            use_container_width=True
        )