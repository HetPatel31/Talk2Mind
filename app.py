import streamlit as st

# Page Config
st.set_page_config(
    page_title="Talk2Mind",
    page_icon="🧠",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
.main-title {
    font-size: 3rem;
    font-weight: 700;
    color: #2563EB;
}

.subtitle {
    font-size: 1.2rem;
    color: #64748B;
}

.feature-card {
    background-color: #1F2937;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #374151;
    color: white;
    min-height: 180px;
}

.feature-card h3 {
    color: white;
}

.feature-card p {
    color: #D1D5DB;
    font-size: 16px;
}

.hero-box {
    padding: 30px;
    border-radius: 16px;
    background: linear-gradient(135deg, #1E3A8A, #2563EB);
    color: white;
    margin-bottom: 20px;
}

.metric-card {
    text-align: center;
    padding: 15px;
    border-radius: 12px;
    background-color: #111827;
    border: 1px solid #374151;
}
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🧠 Talk2Mind")

st.sidebar.info(
    """
    AI-Powered Mental Well-Being Assessment System
    
    Version 1.0
    """
)

st.sidebar.success("✅ Face Analysis")
st.sidebar.success("✅ Voice Analysis")
st.sidebar.success("✅ Questionnaire")

# Hero Section
st.markdown(
    """
    <div class='hero-box'>
        <h1>🧠 Talk2Mind</h1>
        <h3>Understand Your Mental Well-Being with AI</h3>
        <p>
        Analyze facial expressions, voice patterns, and psychological
        assessments to gain personalized mental wellness insights.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.success(
    "Assess your emotional well-being using AI-powered questionnaire, facial emotion recognition, and speech analysis."
)

st.write("")

# Features
st.header("✨ Key Features")
st.caption("Three powerful AI modules working together to assess mental well-being.")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="feature-card">
        <h3>😊 Face Analysis</h3>
        <p>Detect emotional states using computer vision and deep learning.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div class="feature-card">
        <h3>🎤 Voice Analysis</h3>
        <p>Analyze speech characteristics and emotional cues from voice patterns.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        """
        <div class="feature-card">
        <h3>📝 Questionnaire</h3>
        <p>PHQ-9, GAD-7 and lifestyle assessment for mental wellness screening.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

st.write("")

st.header("📊 Platform Highlights")

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric("Emotions", "7")

with m2:
    st.metric("Modules", "3")

with m3:
    st.metric("AI Models", "3")

with m4:
    st.metric("Privacy", "100%")

st.write("")

# Workflow
st.header("🔄 How It Works")

st.markdown("""
1. Complete the mental health questionnaire.
2. Perform facial emotion analysis.
3. Perform voice emotion analysis.
4. AI combines all inputs.
5. Receive a Mental Wellness Score and recommendations.
""")

st.write("")

st.header("⚙️ Technology Stack")

tech1, tech2, tech3, tech4, tech5 = st.columns(5)

tech1.info("PyTorch")
tech2.info("MediaPipe")
tech3.info("Librosa")
tech4.info("OpenCV")
tech5.info("Streamlit")

st.write("")

# Button
st.subheader("Ready to begin?")

if st.button("🚀 Start Assessment", use_container_width=True):
    st.success("Assessment page will be connected in the next step.")

st.write("")
st.write("")

st.divider()
st.caption("Talk2Mind v1.0 | AI-Powered Mental Well-Being Assessment | Built by Het Patel")