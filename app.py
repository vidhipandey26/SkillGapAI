import streamlit as st
import matplotlib.pyplot as plt
import plotly.graph_objects as go

from src.pdf_reader import extract_text_from_pdf
from src.preprocess import clean_text
from src.skill_extractor import extract_skills
from src.semantic_similarity import semantic_similarity

# ------------------ Session State ------------------
if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False


# ------------------ Page Config ------------------
st.set_page_config(page_title="SkillGap AI", layout="centered")

st.title("🚀 SkillGap AI")
st.subheader("AI Resume vs Job Description Analyzer")


# ------------------ Inputs ------------------
uploaded_resume = st.file_uploader(
    "📄 Upload Resume (PDF)",
    type=["pdf"]
)

job_input = st.text_area("💼 Paste Job Description")


# ------------------ Button ------------------
if st.button("Analyze Candidate"):
    st.session_state.analysis_done = True


# ------------------ Analysis Block ------------------
if st.session_state.analysis_done:

    if uploaded_resume is None:
        st.warning("Please upload a resume PDF.")
        st.stop()

    if not job_input:
        st.warning("Please paste a job description.")
        st.stop()

    # Extract resume text
    resume_text = extract_text_from_pdf(uploaded_resume)

    # Clean text
    cleaned_resume = clean_text(resume_text)
    cleaned_job = clean_text(job_input)

    # Extract skills
    resume_skills = extract_skills(cleaned_resume)
    job_skills = extract_skills(cleaned_job)

    # Calculate similarity score
    score = semantic_similarity(cleaned_resume, cleaned_job)
    # Compute matched & missing skills
    matched_skills = list(set(resume_skills) & set(job_skills))
    missing_skills = list(set(job_skills) - set(resume_skills))

    # ------------------ Display Score ------------------
    st.success(f"✅ Match Score: {score}%")

    # ------------------ Gauge Meter ------------------
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={'text': "Candidate Match Score"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'thickness': 0.3},
            'steps': [
                {'range': [0, 40], 'color': "red"},
                {'range': [40, 70], 'color': "orange"},
                {'range': [70, 100], 'color': "green"}
            ],
        }
    ))

    st.plotly_chart(fig_gauge, use_container_width=True)

    # ------------------ Skill Gap Chart ------------------
    labels = ["Matched Skills", "Missing Skills"]
    values = [len(matched_skills), len(missing_skills)]

    fig_bar, ax = plt.subplots()
    ax.bar(labels, values)
    ax.set_ylabel("Skill Count")
    ax.set_title("Skill Gap Analysis")

    st.pyplot(fig_bar)

    # ------------------ Skill Lists ------------------
    col1, col2 = st.columns(2)

    with col1:
        st.write("### ✅ Matched Skills")
        st.write(matched_skills)

    with col2:
        st.write("### ⚠️ Missing Skills")
        st.write(missing_skills)