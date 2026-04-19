import re
from typing import List

SKILLS_DB = ["python","java","javascript","typescript","machine learning","deep learning","nlp","natural language processing","computer vision","tensorflow","pytorch","keras","scikit-learn","xgboost","hugging face","spacy","sql","nosql","postgresql","mysql","mongodb","redis","azure","aws","gcp","google cloud","docker","kubernetes","git","github","pandas","numpy","scipy","matplotlib","plotly","tableau","power bi","statistics","regression","classification","clustering","data science","data analysis","agile","scrum","flask","django","fastapi","streamlit","spark","kafka","airflow","mlflow","llm","transformers","langchain"]

SKILLS_DB_SORTED = sorted(SKILLS_DB, key=len, reverse=True)

def extract_skills(text):
    if not text:
        return []
    text = text.lower()
    found = set()
    for skill in SKILLS_DB_SORTED:
        if " " in skill:
            if skill in text:
                found.add(skill)
        else:
            if re.search(r"\b" + re.escape(skill) + r"\b", text):
                found.add(skill)
    return sorted(list(found))
