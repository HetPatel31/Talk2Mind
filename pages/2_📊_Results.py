

import streamlit as st

st.set_page_config(page_title="Results", page_icon="📊", layout="wide")

st.title("📊 Assessment Results")
st.caption("Mental wellness insights generated from your assessment.")

if "assessment_result" not in st.session_state:
    st.warning("No assessment results found. Please complete the Assessment page first.")
    st.stop()

result = st.session_state["assessment_result"]

# Wellness Score
st.subheader("🧠 Mental Wellness Score")
st.metric("Overall Wellness Score", f"{result['wellness_score']}/100")

st.divider()

# Summary Cards
col1, col2, col3 = st.columns(3)

with col1:
    st.info(f"**Depression Level**\n\n{result['depression_level']}")

with col2:
    st.info(f"**Anxiety Level**\n\n{result['anxiety_level']}")

with col3:
    st.info(f"**Risk Level**\n\n{result['risk_level']}")

st.divider()

# Detailed Scores
st.subheader("📈 Detailed Scores")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Depression Score", result['depression_score'])
c2.metric("Anxiety Score", result['anxiety_score'])
c3.metric("Sleep Score", result['sleep_score'])
c4.metric("Lifestyle Score", result['lifestyle_score'])

st.divider()

# Recommendations
st.subheader("💡 Recommendations")

risk = result['risk_level']

if risk == "Low Risk":
    st.success("""
    • Maintain healthy sleep habits
    • Continue regular exercise
    • Stay socially connected
    • Practice mindfulness and stress management
    """)

elif risk == "Moderate Risk":
    st.warning("""
    • Monitor mood and stress levels
    • Improve sleep quality
    • Increase physical activity
    • Consider speaking with a counselor if symptoms persist
    """)

else:
    st.error("""
    • Consider professional mental health support
    • Talk to trusted friends or family
    • Follow a structured self-care routine
    • Seek immediate help if symptoms become severe
    """)

st.divider()

st.subheader("🚀 Future AI Modules")

st.markdown("""
Coming soon:
- 😊 Face Emotion Analysis
- 🎤 Voice Emotion Analysis
- 🔄 Multimodal Fusion Score
- 📄 PDF Report Generation
""")