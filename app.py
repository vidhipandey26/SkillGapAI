import streamlit as st
import matplotlib.pyplot as plt
import plotly.graph_objects as go

from src.pdf_reader import extract_text_from_pdf
from src.preprocess import clean_text
from src.skill_extractor import extract_skills
from src.semantic_similarity import semantic_similarity


st.set_page_config(page_title="SkillGap AI", layout="centered")

st.title("🚀 SkillGap AI")
st.subheader("AI Resume vs Job Description Analyzer")


uploaded_resume = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

job_input = st.text_area("Paste Job Description")


if st.button("Analyze Candidate", key="analyze_btn"):

    if uploaded_resume is None:
        st.warning("Please upload a resume.")
        st.stop()

    if job_input.strip() == "":
        st.warning("Please paste job description.")
        st.stop()

    # Extract resume text
    resume_text = extract_text_from_pdf(uploaded_resume)

    # Clean text
    cleaned_resume = clean_text(resume_text)
    cleaned_job = clean_text(job_input)

    # Extract skills
    resume_skills = extract_skills(cleaned_resume)
    job_skills = extract_skills(cleaned_job)

    # Calculate similarity
    score = semantic_similarity(cleaned_resume, cleaned_job)
     
    if score > 70:
       st.success("Strong match for this role")
    elif score > 50:
       st.warning("Moderate match — improving a few skills will help")
    else:
       st.error("Low match — several required skills missing")

    matched_skills = list(set(resume_skills) & set(job_skills))
    missing_skills = list(set(job_skills) - set(resume_skills))

    st.success(f"Match Score: {score}%")

    # Gauge chart
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={"text": "Candidate Match Score"},
        gauge={"axis": {"range": [0, 100]}}
    ))

    st.plotly_chart(fig)

    # Skill gap chart
    labels = ["Matched Skills", "Missing Skills"]
    values = [len(matched_skills), len(missing_skills)]

    fig, ax = plt.subplots()

    ax.bar(labels, values, color=["green", "red"])

    ax.set_title("Skill Gap Analysis")
    ax.set_ylabel("Number of Skills")

    st.pyplot(fig)