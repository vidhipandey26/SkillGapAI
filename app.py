import streamlit as st
from src.resume_parser import extract_text_from_pdf
from src.skill_extractor import extract_skills
from src.matcher import match_skills, compute_match_percentage, get_missing_skills
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="SkillGapAI", page_icon="Ì∑†", layout="wide")
st.title("Ì∑† SkillGapAI")
st.markdown("**Semantic Resume √ó Job Description Matcher**")
st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Ì≥Ñ Upload Resume")
    resume_file = st.file_uploader("Upload PDF", type=["pdf"])
with col2:
    st.subheader("Ì≤º Job Description")
    jd_text = st.text_area("Paste job description here", height=200)

if st.button("Ì¥ç Analyze Skill Gap"):
    if not resume_file or not jd_text.strip():
        st.warning("Please upload a resume AND paste a job description.")
    else:
        with st.spinner("Analyzing..."):
            resume_text = extract_text_from_pdf(resume_file)
            resume_skills = extract_skills(resume_text)
            jd_skills = extract_skills(jd_text)
            matched_skills, similarity_scores = match_skills(resume_skills, jd_skills)
            match_pct = compute_match_percentage(matched_skills, jd_skills)
            missing_skills = get_missing_skills(jd_skills, matched_skills)

        st.markdown("---")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Match Score", f"{match_pct:.0f}%")
        c2.metric("Resume Skills", len(resume_skills))
        c3.metric("Matched", len(matched_skills))
        c4.metric("Missing", len(missing_skills))

        fig = go.Figure(go.Bar(
            x=["Matched", "Missing", "JD Skills", "Resume Skills"],
            y=[len(matched_skills), len(missing_skills), len(jd_skills), len(resume_skills)],
            marker_color=["#00f5d4", "#ff61ab", "#7b61ff", "#ffc800"]
        ))
        fig.update_layout(title="Skill Gap Analysis", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("‚úÖ Matched Skills")
        st.write(", ".join(matched_skills) if matched_skills else "None found")

        st.subheader("‚ùå Missing Skills")
        st.write(", ".join(missing_skills) if missing_skills else "Ìæâ You match all skills!")

        if similarity_scores:
            st.subheader("Ì¥¨ Similarity Details")
            df = pd.DataFrame(similarity_scores, columns=["Resume Skill", "JD Skill", "Score"])
            st.dataframe(df, use_container_width=True)
