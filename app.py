import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from resume_parser import extract_text_from_pdf
from skill_extractor import extract_skills
from matcher import match_skills, compute_match_percentage, get_missing_skills
import pandas as pd

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SkillGapAI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #0a0a0f 0%, #0d1117 50%, #0a0f1a 100%);
}

h1, h2, h3 { font-family: 'Syne', sans-serif !important; font-weight: 800 !important; }

.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 3.5rem;
    font-weight: 800;
    background: linear-gradient(90deg, #00f5d4, #7b61ff, #ff61ab);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.2rem;
}

.hero-sub {
    color: #8892a4;
    font-size: 1.1rem;
    margin-bottom: 2rem;
    font-family: 'Space Mono', monospace;
}

.metric-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 1.5rem;
    text-align: center;
    backdrop-filter: blur(10px);
}

.metric-value {
    font-size: 2.8rem;
    font-weight: 800;
    color: #00f5d4;
    font-family: 'Space Mono', monospace;
}

.metric-label {
    color: #8892a4;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 0.3rem;
}

.skill-tag-match {
    display: inline-block;
    background: rgba(0,245,212,0.12);
    border: 1px solid rgba(0,245,212,0.3);
    color: #00f5d4;
    border-radius: 20px;
    padding: 4px 14px;
    margin: 4px;
    font-size: 0.82rem;
    font-family: 'Space Mono', monospace;
}

.skill-tag-miss {
    display: inline-block;
    background: rgba(255,97,171,0.1);
    border: 1px solid rgba(255,97,171,0.3);
    color: #ff61ab;
    border-radius: 20px;
    padding: 4px 14px;
    margin: 4px;
    font-size: 0.82rem;
    font-family: 'Space Mono', monospace;
}

.section-title {
    font-size: 1.3rem;
    font-weight: 700;
    color: #e2e8f0;
    border-left: 3px solid #7b61ff;
    padding-left: 12px;
    margin: 1.5rem 0 1rem 0;
}

div[data-testid="stFileUploader"] {
    border: 2px dashed rgba(123,97,255,0.4) !important;
    border-radius: 12px !important;
    background: rgba(123,97,255,0.04) !important;
    padding: 1rem !important;
}

div[data-testid="stTextArea"] textarea {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    color: #e2e8f0 !important;
    border-radius: 12px !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.85rem !important;
}

.stButton > button {
    background: linear-gradient(135deg, #7b61ff, #00f5d4) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.7rem 2.5rem !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    letter-spacing: 0.05em !important;
    transition: all 0.2s ease !important;
    width: 100% !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(123,97,255,0.4) !important;
}

.warning-box {
    background: rgba(255,200,0,0.08);
    border: 1px solid rgba(255,200,0,0.25);
    border-radius: 10px;
    padding: 0.8rem 1.2rem;
    color: #ffc800;
    font-family: 'Space Mono', monospace;
    font-size: 0.82rem;
    margin-top: 1rem;
}
</style>
""", unsafe_allow_html=True)


# ─── Header ─────────────────────────────────────────────────────────────────
st.markdown('<div class="hero-title">SkillGapAI</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">// semantic resume × job description matcher</div>', unsafe_allow_html=True)

st.markdown("---")

# ─── Input Section ──────────────────────────────────────────────────────────
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown('<div class="section-title">📄 Resume Upload</div>', unsafe_allow_html=True)
    resume_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"], label_visibility="collapsed")
    if resume_file:
        st.success(f"✅ Loaded: `{resume_file.name}`")

with col2:
    st.markdown('<div class="section-title">💼 Job Description</div>', unsafe_allow_html=True)
    jd_text = st.text_area(
        "Paste the job description here",
        height=200,
        placeholder="e.g. We are looking for a Python developer with experience in ML, Azure, SQL...",
        label_visibility="collapsed"
    )

st.markdown("<br>", unsafe_allow_html=True)
_, btn_col, _ = st.columns([1, 2, 1])
with btn_col:
    analyze_btn = st.button("🔍 Analyze Skill Gap")


# ─── Analysis ───────────────────────────────────────────────────────────────
if analyze_btn:
    if not resume_file or not jd_text.strip():
        st.warning("⚠️ Please upload a resume AND paste a job description before analyzing.")
    else:
        with st.spinner("Extracting text and running semantic matching..."):

            # Extract
            resume_text = extract_text_from_pdf(resume_file)
            resume_skills = extract_skills(resume_text)
            jd_skills = extract_skills(jd_text)

            if not resume_skills:
                st.error("❌ Could not extract skills from the resume. Try a different PDF.")
                st.stop()
            if not jd_skills:
                st.error("❌ Could not extract skills from the job description.")
                st.stop()

            # Match
            matched_skills, similarity_scores = match_skills(resume_skills, jd_skills)
            match_pct = compute_match_percentage(matched_skills, jd_skills)
            missing_skills = get_missing_skills(jd_skills, matched_skills)

        # ── Metrics ─────────────────────────────────────────────────────────
        st.markdown("---")
        st.markdown('<div class="section-title">📊 Analysis Results</div>', unsafe_allow_html=True)

        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{match_pct:.0f}%</div>
                <div class="metric-label">Match Score</div>
            </div>""", unsafe_allow_html=True)
        with m2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value" style="color:#7b61ff">{len(resume_skills)}</div>
                <div class="metric-label">Resume Skills</div>
            </div>""", unsafe_allow_html=True)
        with m3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value" style="color:#00f5d4">{len(matched_skills)}</div>
                <div class="metric-label">Matched</div>
            </div>""", unsafe_allow_html=True)
        with m4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value" style="color:#ff61ab">{len(missing_skills)}</div>
                <div class="metric-label">Missing</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Bar Chart ────────────────────────────────────────────────────────
        chart_col, skills_col = st.columns([3, 2], gap="large")

        with chart_col:
            st.markdown('<div class="section-title">📉 Skill Gap Breakdown</div>', unsafe_allow_html=True)

            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=["Matched Skills", "Missing Skills", "Total JD Skills", "Resume Skills"],
                y=[len(matched_skills), len(missing_skills), len(jd_skills), len(resume_skills)],
                marker=dict(
                    color=["#00f5d4", "#ff61ab", "#7b61ff", "#ffc800"],
                    line=dict(color="rgba(255,255,255,0.1)", width=1)
                ),
                text=[len(matched_skills), len(missing_skills), len(jd_skills), len(resume_skills)],
                textposition="outside",
                textfont=dict(color="white", family="Space Mono", size=13)
            ))
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#8892a4", family="Syne"),
                xaxis=dict(gridcolor="rgba(255,255,255,0.05)", tickfont=dict(color="#8892a4")),
                yaxis=dict(gridcolor="rgba(255,255,255,0.05)", tickfont=dict(color="#8892a4")),
                margin=dict(t=20, b=20, l=10, r=10),
                height=320,
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)

            # Similarity gauge
            fig2 = go.Figure(go.Indicator(
                mode="gauge+number",
                value=match_pct,
                number={"suffix": "%", "font": {"color": "#00f5d4", "family": "Space Mono", "size": 36}},
                gauge={
                    "axis": {"range": [0, 100], "tickcolor": "#8892a4"},
                    "bar": {"color": "#7b61ff"},
                    "steps": [
                        {"range": [0, 40], "color": "rgba(255,97,171,0.15)"},
                        {"range": [40, 70], "color": "rgba(255,200,0,0.1)"},
                        {"range": [70, 100], "color": "rgba(0,245,212,0.1)"},
                    ],
                    "threshold": {"line": {"color": "#00f5d4", "width": 3}, "value": match_pct}
                },
                title={"text": "Overall Match", "font": {"color": "#8892a4", "family": "Syne"}}
            ))
            fig2.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#8892a4"),
                height=250,
                margin=dict(t=30, b=10, l=30, r=30)
            )
            st.plotly_chart(fig2, use_container_width=True)

        with skills_col:
            st.markdown('<div class="section-title">✅ Matched Skills</div>', unsafe_allow_html=True)
            if matched_skills:
                tags = "".join([f'<span class="skill-tag-match">{s}</span>' for s in matched_skills])
                st.markdown(tags, unsafe_allow_html=True)
            else:
                st.info("No matched skills found.")

            st.markdown('<div class="section-title">❌ Missing Skills</div>', unsafe_allow_html=True)
            if missing_skills:
                tags = "".join([f'<span class="skill-tag-miss">{s}</span>' for s in missing_skills])
                st.markdown(tags, unsafe_allow_html=True)
                st.markdown("""
                <div class="warning-box">
                ⚡ Tip: Upskill in these areas to improve your match score.
                </div>
                """, unsafe_allow_html=True)
            else:
                st.success("🎉 You match all required skills!")

        # ── Similarity scores table ──────────────────────────────────────────
        if similarity_scores:
            st.markdown('<div class="section-title">🔬 Semantic Similarity Details</div>', unsafe_allow_html=True)
            df = pd.DataFrame(similarity_scores, columns=["Resume Skill", "JD Skill", "Similarity"])
            df["Similarity"] = df["Similarity"].map(lambda x: f"{x:.2f}")
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )