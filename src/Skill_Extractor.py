import re
from typing import List

SKILLS_DB = [
    "python", "java", "javascript", "typescript", "c++", "c#", "go", "rust",
    "kotlin", "swift", "scala", "r", "matlab", "php", "ruby", "bash",
    "machine learning", "deep learning", "neural networks", "nlp",
    "natural language processing", "computer vision", "reinforcement learning",
    "generative ai", "large language models", "llm", "transformers",
    "tensorflow", "pytorch", "keras", "scikit-learn", "xgboost", "lightgbm",
    "hugging face", "spacy", "nltk", "opencv", "langchain",
    "sql", "nosql", "postgresql", "mysql", "mongodb", "redis", "elasticsearch",
    "azure", "microsoft azure", "azure ml", "azure machine learning",
    "azure blob storage", "azure devops", "azure functions", "azure openai",
    "aws", "amazon web services", "ec2", "s3", "lambda", "sagemaker",
    "gcp", "google cloud", "bigquery", "vertex ai",
    "docker", "kubernetes", "ci/cd", "github actions", "jenkins", "terraform",
    "mlflow", "airflow", "fastapi", "flask", "django", "streamlit",
    "rest api", "graphql", "microservices", "react", "node.js",
    "git", "github", "gitlab", "spark", "apache spark", "kafka",
    "pandas", "numpy", "scipy", "matplotlib", "plotly", "tableau", "power bi",
    "statistics", "probability", "linear algebra", "hypothesis testing",
    "regression", "classification", "clustering", "time series",
    "data science", "data analysis", "data engineering", "etl",
    "agile", "scrum", "communication", "leadership", "problem solving",
]

_SORTED_SKILLS = sorted(SKILLS_DB, key=len, reverse=True)

def extract_skills(text: str) -> List[str]:
    if not text:
        return []
    try:
        text = text.encode("utf-8", errors="ignore").decode("utf-8", errors="ignore")
        text_lower = text.lower()
    except Exception:
        return []
    found = set()
    for skill in _SORTED_SKILLS:
        if " " in skill:
            if skill in text_lower:
                found.add(skill)
        else:
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                found.add(skill)
    return sorted(list(found))
