

import streamlit as st
from modules.questionnaire.questionnaire import QuestionnaireAssessment

st.set_page_config(page_title="Assessment", page_icon="📝", layout="wide")

st.title("📝 Mental Health Assessment")
st.caption("Complete the questionnaire to generate your wellness assessment.")

q = QuestionnaireAssessment()

options = {
    "Not at all": 0,
    "Several days": 1,
    "More than half the days": 2,
    "Nearly every day": 3
}

st.header("PHQ-9 Depression Assessment")
phq_responses = []

for i, question in enumerate(q.phq9_questions, start=1):
    response = st.radio(
        f"{i}. {question}",
        options=list(options.keys()),
        key=f"phq_{i}"
    )
    phq_responses.append(options[response])

st.divider()

st.header("GAD-7 Anxiety Assessment")
gad_responses = []

for i, question in enumerate(q.gad7_questions, start=1):
    response = st.radio(
        f"{i}. {question}",
        options=list(options.keys()),
        key=f"gad_{i}"
    )
    gad_responses.append(options[response])

st.divider()

st.header("Lifestyle Assessment")

sleep_hours = st.slider(
    "Average Sleep Hours",
    min_value=0,
    max_value=12,
    value=7
)

exercise_score = st.slider(
    "Exercise Frequency",
    min_value=0,
    max_value=10,
    value=5
)

social_score = st.slider(
    "Social Interaction",
    min_value=0,
    max_value=10,
    value=5
)

stress_score = st.slider(
    "Weekly Stress Level",
    min_value=0,
    max_value=10,
    value=5
)

if st.button("🧠 Generate Assessment", use_container_width=True):

    sleep_score = q.calculate_sleep_score(
        sleep_hours=sleep_hours,
        refreshed_score=3,
        difficulty_score=1
    )

    lifestyle_score = q.calculate_lifestyle_score(
        exercise_score,
        social_score,
        stress_score
    )

    result = q.generate_assessment(
        phq_responses,
        gad_responses,
        sleep_score,
        lifestyle_score
    )

    st.session_state["assessment_result"] = result

    st.session_state["wellness_score"] = result["wellness_score"]
    st.session_state["risk_level"] = result["risk_level"]

    st.session_state["depression_score"] = result["depression_score"]
    st.session_state["anxiety_score"] = result["anxiety_score"]

    st.session_state["depression_level"] = result["depression_level"]
    st.session_state["anxiety_level"] = result["anxiety_level"]

    st.success("Assessment Generated Successfully")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Wellness Score", result["wellness_score"])

    with col2:
        st.metric("Depression", result["depression_level"])

    with col3:
        st.metric("Anxiety", result["anxiety_level"])

    st.info(f"Risk Level: {result['risk_level']}")